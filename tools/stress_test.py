#!/usr/bin/env python

"""Stress test script to simulate multiple Zoom participants using Selenium
This script launches multiple browser instances to join a Zoom meeting as different participants.
It handles joining the meeting, setting audio preferences, and cleaning up browsers on exit.
"""

import argparse
import logging
import os
import re
import signal
import tempfile
import threading
import time

import names


from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Rich logging
from rich.logging import RichHandler

# Global event to signal shutdown
shutdown_event = threading.Event()


def signal_handler(_signum, _frame):
    """Handle Ctrl+C and other signals to gracefully close browsers"""
    logger = logging.getLogger(__name__)
    logger.info("Received interrupt signal, shutting down browsers...")
    shutdown_event.set()
    # Let the main thread handle the exit
    # No sys.exit(0) here


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            logging.FileHandler("stress_test.log"),
            RichHandler(rich_tracebacks=True),
        ],
    )

    # Suppress webdriver_manager and WDM logs
    logging.getLogger("WDM").setLevel(logging.WARNING)
    logging.getLogger("webdriver_manager").setLevel(logging.WARNING)


def create_chrome_options(user_data_dir=None):
    """Create Chrome options for automated testing"""
    options = Options()

    # Use a unique user data directory for each instance
    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")

    # Add arguments to make automation more reliable
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")

    # Auto-allow microphone and camera permissions
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    # Optional: Run in headless mode (comment out if you want to see browsers)
    options.add_argument("--headless")

    # Disable notifications and popups
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    # Set permissions for microphone and camera
    prefs = {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 1,
    }
    options.add_experimental_option("prefs", prefs)

    # Set user agent to avoid detection
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    return options


def join_meeting_as_participant(
    meeting_url, participant_name, participant_id, duration_seconds=1800
):
    """Join a Zoom meeting as a specific participant using Selenium"""
    logger = logging.getLogger(__name__)
    driver = None

    try:

        logger.info(
            "Starting participant %s (ID: %s)", participant_name, participant_id
        )

        temp_dir = tempfile.mkdtemp()
        user_data_dir = os.path.join(temp_dir, f"chrome_user_data_{participant_id}")
        options = create_chrome_options(user_data_dir)

        # Initialize Chrome driver with automatic driver management
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.set_window_size(800, 600)  # Construct join URL with participant name
        join_url = f"{meeting_url}&uname={participant_name}"

        direct_url = try_construct_direct_url(meeting_url, participant_name)
        if direct_url:
            logger.info("Using direct web app URL for %s", participant_name)
            driver.get(direct_url)
        else:
            logger.info("Navigating to regular URL: %s", join_url)
            driver.get(join_url)

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Since we're using direct URLs, we should be in the meeting interface
        # Just wait a moment for everything to load and handle join/audio
        time.sleep(2)
        logger.info("Page loaded for %s, handling meeting join", participant_name)

        # Wait for meeting interface to load
        time.sleep(3)

        try:
            # Handle joining the meeting and audio preferences
            join_successful = handle_meeting_join_and_audio(
                driver, participant_name, logger
            )

            if join_successful:
                logger.info(
                    "[green]Participant %s (id: %s) successfully joined the meeting[/green]",
                    participant_name,
                    participant_id,
                    extra=({"markup": True}),
                )
                # Keep browser open for the duration of the test, but check for shutdown
                end_time = time.time() + duration_seconds
                while time.time() < end_time and not shutdown_event.is_set():
                    time.sleep(1)  # Check for shutdown every second

                if shutdown_event.is_set():
                    logger.info(
                        "Shutdown signal received, closing browser for %s",
                        participant_name,
                    )
                else:
                    logger.info(
                        "Duration ended for %s, closing browser.", participant_name
                    )

            else:
                logger.error(
                    "[red]Participant %s failed to join the meeting[/red]",
                    participant_name,
                    extra=({"markup": True}),
                )
                time.sleep(10)  # Keep browser open briefly for debugging

        except TimeoutException:
            logger.error(
                "[yellow]Timeout while trying to join meeting for %s[/yellow]",
                participant_name,
                extra=({"markup": True}),
            )
        except WebDriverException as e:
            logger.error(
                "WebDriver error during meeting join for %s: %s",
                participant_name,
                str(e),
            )
        except Exception as e:
            logger.error(
                "Unexpected error during meeting join for %s: %s",
                participant_name,
                str(e),
            )
            raise e

    except WebDriverException as e:
        logger.error("WebDriver error for participant %s: %s", participant_name, str(e))
    except Exception as e:
        logger.error(
            "Unexpected error for participant %s: %s", participant_name, str(e)
        )
        raise e
    finally:
        if driver:
            # Suppress noisy connection errors from urllib3 and selenium during shutdown
            if shutdown_event.is_set():
                logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)
                logging.getLogger(
                    "selenium.webdriver.remote.remote_connection"
                ).setLevel(logging.ERROR)
            try:
                driver.quit()
                logger.info("Browser closed for participant %s", participant_name)
            except WebDriverException as e:
                if "Connection refused" in str(e) or "Connection reset" in str(e):
                    logger.info(
                        "Browser for %s already closed or connection reset during shutdown.",
                        participant_name,
                    )
                else:
                    logger.error(
                        "Error closing browser for %s: %s", participant_name, str(e)
                    )
            except (OSError, RuntimeError) as e:
                # OSError: e.g., browser process already dead, pipe closed
                # RuntimeError: e.g., internal Selenium/driver state errors
                logger.error(
                    "OS/Runtime error closing browser for %s: %s",
                    participant_name,
                    str(e),
                )


def try_join_from_browser(driver, participant_name, logger):
    """Helper function to try different methods of joining from browser"""
    try:
        # Look for and click "Join from Your Browser" link
        join_browser_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Join from Your Browser"))
        )
        logger.info("Clicking 'Join from Your Browser' for %s", participant_name)
        join_browser_link.click()
        return True

    except TimeoutException:
        # Try alternative selectors
        try:
            join_browser_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "browser"))
            )
            join_browser_link.click()
            return True
        except TimeoutException:
            try:
                # Try looking for "Launch Meeting" button
                launch_meeting_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(), 'Launch Meeting')]")
                    )
                )
                launch_meeting_btn.click()
                return True
            except TimeoutException:
                logger.warning(
                    "Could not find any join button for %s", participant_name
                )
                return False


def try_construct_direct_url(meeting_url, participant_name):
    """Try to construct a direct web app URL from a regular Zoom meeting URL"""

    # Extract meeting ID and password from the URL
    # Pattern: https://us06web.zoom.us/j/MEETINGID?pwd=PASSWORD
    match = re.search(r"/j/(\d+)\?pwd=([^&]+)", meeting_url)
    if match:
        meeting_id = match.group(1)
        password = match.group(2)

        # Construct the direct web app URL
        direct_url = f"https://app.zoom.us/wc/{meeting_id}/"
        direct_url += f"join?fromPWA=1&pwd={password}&uname={participant_name}"
        return direct_url

    return None


def handle_zoom_page_navigation(driver, participant_name, logger):
    """Handle navigation on the regular Zoom page to get to the web app"""
    # Check if we got a popup asking to open Zoom app
    try:
        # Look for the "Cancel" button in the popup and click it to dismiss
        cancel_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(text(), 'Cancel') or contains(text(), 'cancel')]",
                )
            )
        )
        logger.info("Dismissing 'Open zoom.us?' popup for %s", participant_name)
        cancel_button.click()
        time.sleep(1)
    except TimeoutException:
        logger.info("No app popup found for %s", participant_name)

    # Try to find a direct web app link first
    try:
        # Look for links that go directly to app.zoom.us
        web_app_links = driver.find_elements(
            By.XPATH, "//a[contains(@href, 'app.zoom.us/wc')]"
        )
        if web_app_links:
            logger.info("Found direct web app link for %s", participant_name)
            web_app_links[0].click()
        else:
            # Fallback: try to construct direct URL or look for "Join from Browser"
            try_join_from_browser(driver, participant_name, logger)
    except WebDriverException as e:
        logger.warning(
            f"WebDriver error during web app link search for {participant_name}: {str(e)}"
        )
        try_join_from_browser(driver, participant_name, logger)


def handle_meeting_join_and_audio(driver, participant_name, logger):
    """Handle joining the meeting and setting audio preferences (muted)"""

    # First, let's debug what page we're actually on
    current_url = driver.current_url
    page_title = driver.title
    logger.info("Current URL for %s: %s", participant_name, current_url)
    logger.info("Page title for %s: %s", participant_name, page_title)

    # Check if we're on the "Enter Meeting Info" page with multiple detection methods

    # Method 1: Look for the "Enter Meeting Info" text
    meeting_info_text = driver.find_elements(
        By.XPATH, "//*[contains(text(), 'Enter Meeting Info')]"
    )

    # Method 2: Look for the name input field
    name_input = driver.find_elements(
        By.XPATH,
        "//input[contains(@placeholder, 'name') or contains(@placeholder, 'Name')]",
    )

    # Method 3: Look for the Join button
    join_button_elements = driver.find_elements(
        By.XPATH, "//button[contains(text(), 'Join')]"
    )

    # Method 4: Look for "Your Name" label
    name_label = driver.find_elements(By.XPATH, "//*[contains(text(), 'Your Name')]")

    logger.info(
        "Detection results for %s: meeting_info_text=%d,"
        " name_input=%d, join_button=%d, name_label=%d",
        participant_name,
        len(meeting_info_text),
        len(name_input),
        len(join_button_elements),
        len(name_label),
    )

    # If we found any of these elements, we're likely on the Enter Meeting Info page
    if meeting_info_text or name_input or join_button_elements or name_label:
        logger.info("Detected meeting join page for %s", participant_name)

        # Step 1: Click the Mute button (it should be visible in the preview area)
        mute_clicked = False
        try:
            # Wait for preview area to load
            time.sleep(2)

            # Look for the mute button - try multiple selectors
            mute_selectors = [
                "//button[contains(text(), 'Mute') and not(contains(text(), 'Unmute'))]",
                "//button[contains(@aria-label, 'Mute') "
                "and not(contains(@aria-label, 'Unmute'))]",
                "//button[contains(@title, 'Mute') and not(contains(@title, 'Unmute'))]",
                "//button[contains(@class, 'mute') and not(contains(@class, 'unmute'))]",
                "//button[contains(@aria-label, 'mute') and "
                "not(contains(@aria-label, 'unmute'))]",
            ]

            # First, check if we're already muted by looking for "Unmute" button
            already_muted = False
            try:
                unmute_check = driver.find_elements(
                    By.XPATH,
                    "//button[contains(text(), 'Unmute') or contains(@aria-label, 'Unmute')]",
                )
                if unmute_check:
                    already_muted = True
                    logger.info("Participant %s is already muted", participant_name)
            except WebDriverException as e:
                logger.warning(
                    f"WebDriver error during mute check for {participant_name}: {str(e)}"
                )

            if not already_muted:
                for selector in mute_selectors:
                    try:
                        mute_buttons = driver.find_elements(By.XPATH, selector)
                        for mute_button in mute_buttons:
                            if mute_button.is_enabled() and mute_button.is_displayed():
                                mute_button.click()
                                logger.info(
                                    "Clicked Mute button using selector '%s' for %s",
                                    selector,
                                    participant_name,
                                )
                                mute_clicked = True
                                time.sleep(1)
                                break
                        if mute_clicked:
                            break
                    except WebDriverException as e:
                        logger.warning(
                            f"WebDriver error at mute button search: {participant_name}: {str(e)}"
                        )
                        continue

            if not mute_clicked and not already_muted:
                logger.warning(
                    "Could not find or click mute button for %s, participant may join unmuted",
                    participant_name,
                )
            elif already_muted:
                mute_clicked = True

        except WebDriverException as e:
            logger.warning(
                f"WebDriver error trying to mute {participant_name}: {str(e)}"
            )

        # Step 2: Click the Join button - try multiple approaches
        join_success = False
        try:
            # Wait a bit more for the page to fully load
            time.sleep(5)  # Increased wait time

            # Check if we need to switch to an iframe
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            logger.debug(f"Found {len(iframes)} iframes on page for {participant_name}")

            if iframes:
                for i, iframe in enumerate(iframes):
                    try:
                        driver.switch_to.frame(iframe)
                        logger.debug(f"Switched to iframe {i} for {participant_name}")

                        # Check elements in this iframe
                        frame_buttons = driver.find_elements(By.TAG_NAME, "button")
                        frame_inputs = driver.find_elements(By.TAG_NAME, "input")
                        logger.debug(
                            f"In iframe {i}: {len(frame_buttons)} "
                            f"buttons, {len(frame_inputs)} inputs"
                        )

                        # Check for mute button in iframe if we haven't muted yet
                        if frame_buttons and not mute_clicked:
                            try:
                                # Look for mute button in iframe
                                iframe_mute_selectors = [
                                    "//button[contains(text(), 'Mute') and"
                                    " not(contains(text(), 'Unmute'))]",
                                    "//button[contains(@aria-label, 'Mute') and "
                                    "not(contains(@aria-label, 'Unmute'))]",
                                ]

                                for selector in iframe_mute_selectors:
                                    iframe_mute_buttons = driver.find_elements(
                                        By.XPATH, selector
                                    )
                                    for mute_btn in iframe_mute_buttons:
                                        if (
                                            mute_btn.is_enabled()
                                            and mute_btn.is_displayed()
                                        ):
                                            mute_btn.click()
                                            logger.info(
                                                "Clicked Mute button in "
                                                f"iframe {i} for {participant_name}",
                                            )
                                            mute_clicked = True
                                            time.sleep(1)
                                            break
                                    if mute_clicked:
                                        break
                            except WebDriverException as e:
                                logger.warning(
                                    f"WebDriver error at iframe mute: {participant_name}: {str(e)}"
                                )

                        if frame_buttons:
                            for j, btn in enumerate(frame_buttons[:5]):
                                btn_text = btn.text.strip()
                                btn_type = btn.get_attribute("type")
                                logger.debug(
                                    f"Iframe {i} Button {j}: "
                                    f"text='{btn_text}', type='{btn_type}'"
                                )
                            break  # Found buttons, stay in this iframe
                        else:
                            driver.switch_to.default_content()  # Switch back if no buttons
                    except WebDriverException as e:
                        logger.info(f"Could not switch to iframe {i}: {str(e)}")
                        driver.switch_to.default_content()

            # Debug: Let's see what buttons are actually on the page
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
            all_links = driver.find_elements(By.TAG_NAME, "a")

            logger.debug(
                f"Debug for {participant_name}: Found {len(all_buttons)} "
                f"buttons, {len(all_inputs)} inputs, {len(all_links)} links"
            )

            for i, btn in enumerate(all_buttons[:10]):  # Show first 10 buttons
                btn_text = btn.text.strip()
                btn_type = btn.get_attribute("type")
                btn_class = btn.get_attribute("class")
                btn_aria = btn.get_attribute("aria-label")
                logger.debug(
                    f"Button {i}: text='{btn_text}', type='{btn_type}', "
                    f"class='{btn_class}', aria-label='{btn_aria}'"
                )

            # Try different selectors for the join button
            join_selectors = [
                "//button[contains(text(), 'Join')]",
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), 'join')]",
                "//input[@type='submit' and contains(@value, 'Join')]",
                "//a[contains(text(), 'Join')]",
                "//button[@type='submit']",
                "//button[contains(@class, 'join')]",
                "//*[contains(text(), 'Join') and (name()='button' or "
                "name()='input' or name()='a')]",
            ]

            for selector in join_selectors:
                try:
                    join_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    join_button.click()
                    logger.info(
                        "Successfully clicked Join button using "
                        f"selector '{selector}' for {participant_name}"
                    )
                    join_success = True
                    time.sleep(3)  # Wait for meeting to load
                    break
                except TimeoutException:
                    logger.warning(
                        "[yellow]Selector '%s' did not find a "
                        "clickable element for %s[/yellow]",
                        selector,
                        participant_name,
                        extra={"markup": True},
                    )
                    continue

            if not join_success:
                logger.error(
                    "[red]Could not find any clickable Join button for %s[/red]",
                    participant_name,
                    extra={"markup": True},
                )
                return False
            else:
                return True

        except WebDriverException as e:
            logger.error(
                f"WebDriver error clicking Join button for {participant_name}: {str(e)}"
            )
            return False

    else:
        # We're not on the "Enter Meeting Info" page, try other strategies
        logger.info(
            f"Not on Enter Meeting Info page for {participant_name}, trying other join methods"
        )
        return try_other_join_methods(driver, participant_name, logger)

    # No stray except or closing brace here; all exceptions are handled above.


def try_other_join_methods(driver, participant_name, logger):
    """Try alternative methods for joining when not on the standard Enter Meeting Info page"""

    # Strategy 1: Look for "Join Audio by Computer" button
    try:
        join_audio_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Join Audio')]")
            )
        )
        join_audio_btn.click()
        logger.info(f"Clicked 'Join Audio' for {participant_name}")
        time.sleep(2)
        return True
    except TimeoutException:
        pass

    # Strategy 2: Look for generic "Join" button
    try:
        join_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(text(), 'Join') and not(contains(text(), 'Audio'))]",
                )
            )
        )
        join_btn.click()
        logger.info(f"Clicked main 'Join' button for {participant_name}")
        time.sleep(2)
        return True
    except TimeoutException:
        pass

    # Strategy 3: Look for "Enter" or "Start" buttons
    try:
        enter_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(text(), 'Enter') or contains(text(), 'Start')]",
                )
            )
        )
        enter_btn.click()
        logger.info(f"Clicked 'Enter/Start' button for {participant_name}")
        time.sleep(2)
        return True
    except TimeoutException:
        pass

    logger.warning(f"Could not find any join button for {participant_name}")
    return False


def main():
    """Launch multiple browser instances to simulate Zoom participants"""
    setup_logging()
    logger = logging.getLogger(__name__)

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser(
        description="Launch multiple browser instances to simulate Zoom participants using Selenium"
    )
    parser.add_argument(
        "--meeting-url",
        required=True,
        help="Join link for the Zoom meeting (e.g. https://zoom.us/wc/<id>/join)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of simulated participants (default: 5, be cautious with high numbers)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay in seconds between launching participants (default: 2.0)",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Launch participants in parallel (faster but more resource intensive)",
    )
    parser.add_argument(
        "--parallel-thread-count",
        type=int,
        default=12,
        help="Maximum number of threads to start simultaneously"
        " when using --parallel (default: 12)",
    )
    parser.add_argument(
        "--parallel-thread-delay",
        type=int,
        default=30,
        help="Delay in seconds before starting next batch of "
        "threads when using --parallel (default: 30)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=1800,  # 30 minutes in seconds
        help="Duration in seconds each participant stays in meeting (default: 1800 = 30 minutes)",
    )

    args = parser.parse_args()

    logger.info("Starting stress test with %d participants", args.count)
    logger.info("Meeting URL: %s", args.meeting_url)
    logger.info("Delay between participants: %s seconds", args.delay)
    logger.info("Parallel mode: %s", args.parallel)
    if args.parallel:
        logger.info("Parallel thread count: %d", args.parallel_thread_count)
        logger.info("Parallel thread delay: %d seconds", args.parallel_thread_delay)
    logger.info(
        "Duration per participant: %d seconds (%.1f minutes)",
        args.duration,
        args.duration / 60.0,
    )

    threads = []

    if args.parallel:
        # Launch participants in batches with controlled concurrency
        logger.info(
            "Launching participants in batches of %d", args.parallel_thread_count
        )

        for batch_start in range(1, args.count + 1, args.parallel_thread_count):
            batch_end = min(batch_start + args.parallel_thread_count, args.count + 1)
            batch_threads = []

            logger.info(
                "Starting batch: participants %d to %d", batch_start, batch_end - 1
            )

            # Start threads in this batch
            for i in range(batch_start, batch_end):
                participant_name = names.get_full_name()

                thread = threading.Thread(
                    target=join_meeting_as_participant,
                    args=(args.meeting_url, participant_name, i, args.duration),
                )
                threads.append(thread)
                batch_threads.append(thread)
                thread.start()

                # Small delay between thread starts to avoid overwhelming the system
                time.sleep(0.5)

            # If this isn't the last batch, wait for the parallel thread delay
            if batch_end <= args.count:
                logger.info(
                    "Batch started, waiting %d seconds before next batch...",
                    args.parallel_thread_delay,
                )
                time.sleep(args.parallel_thread_delay)
    else:
        # Launch participants sequentially but with threading
        # so they can all stay in meeting together
        for i in range(1, args.count + 1):
            participant_name = names.get_full_name()

            thread = threading.Thread(
                target=join_meeting_as_participant,
                args=(args.meeting_url, participant_name, i, args.duration),
            )
            threads.append(thread)
            thread.start()

            # Wait for the delay before starting next participant
            if i < args.count:  # Don't wait after the last participant
                time.sleep(args.delay)

    # Wait for all threads to complete (both parallel and sequential modes)
    logger.info("Waiting for all participants to complete...")
    for thread in threads:
        thread.join()

    logger.info("[green]Stress test completed[/green]", extra={"markup": True})


if __name__ == "__main__":
    main()
