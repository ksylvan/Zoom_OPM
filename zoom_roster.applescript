#!/usr/bin/osascript

(*
 Copyright (c) 2023 Kayvan A. Sylvan

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *)

(**
 * This code creates two files in the directory that the script in run, log.txt and roster.txt.
 * It checks if the Zoom app is running, if we are in a Zoom meeting, and if needed,
 * activates the Participants pane.
 * 
 * It then writes the names of the participants to the roster.txt file.
 *)

-- Global properties

property scriptName : "Zoom Roster"
property appName : "zoom.us"
property appVersion : missing value
property topZoomWindow : "Zoom"
property meetingWindow : "Zoom Meeting"
property participantsOpen : "Show Manage Participants"
property participantsClose : "Close Manage Participants"
property inMeeting : false

-- These two files are created in the logs/ subdirectory of the directory where the script is run.
-- The pattern of filenames: logs/20231014-log.txt and logs/20231014-roster.txt
-- This makes it easy to store and index the logs at a later time.
property logFile : "log.txt"
property meetingRoster : "roster.txt"

on todayYMD()
	set [_day, _month, _year] to [day, month, year] of (current date)
	set _month to _month * 1 --> 3
	set _month to text -1 thru -2 of ("0" & _month) --> "03"
	set _day to text -1 thru -2 of ("0" & _day)
	set result to _year & _month & _day
	return result
end todayYMD

on setUpFiles()
 (*
  * This code sets up two files, logFile and meetingRoster, in the "logs/" subdirectory
  * of the containing directory of the script. It sets up the files as global POSIX file handles.
  * The files are named with a prefix of the current date in YYYMMDD format for easy indexing.
  *)
	tell application "Finder"
		set _logDir to container of (path to me)
		if not (exists folder "logs" of _logDir) then
        	make new folder at _logDir with properties {name:"logs"}
    	end if
	end tell
	set _logDir to POSIX path of (_logDir as text)
	set _prefix to my todayYMD()
	set logFile to POSIX file (_logDir & "logs/" & _prefix & "-" & logFile)
	set meetingRoster to POSIX file (_logDir & "logs/" & _prefix & "-" & meetingRoster)
	tell application "Finder"
		do shell script "echo 'Your log message here'"
	end tell
end setUpFiles

on stringStartsWith(theSubstring, theString)
	(*
	-- Usage:
	set theString to "Hello, world!"
	set theSubstring to "Hello"
	set doesStartWith to stringStartsWith(theSubstring, theString)
	log doesStartWith -- logs "true"
	*)
	set tid to AppleScript's text item delimiters -- save the current delimiters
	set AppleScript's text item delimiters to theSubstring -- set the delimiter to the substring
	set textItems to text items of theString -- split the string by the substring
	set AppleScript's text item delimiters to tid -- restore the original delimiters
	return (count of textItems) > 1 and (item 1 of textItems is "")
end stringStartsWith

on formatDateTime(theDateTime)
	set [_day, _month, _year, _hours, _minutes, _seconds] to [day, month, year, hours, minutes, seconds] of theDateTime
	set _month to _month * 1 --> 3
	set _month to text -1 thru -2 of ("0" & _month) --> "03"
	set _day to text -1 thru -2 of ("0" & _day)
	set _hours to text -1 thru -2 of ("0" & _hours) --> "05"
	set _minutes to text -1 thru -2 of ("0" & _minutes)
	set _seconds to text -1 thru -2 of ("0" & _seconds)
	set result to _month & "/" & _day & "/" & _year & " " & _hours & ":" & _minutes & ":" & _seconds
	return result
end formatDateTime

on logMessage(message, filePath)
	(*
    -- Usage:
    set logFilePath to (path to desktop as string) & "logfile.txt" -- Path to the log file
    my logMessage("This is a log message.", logFilePath)
    *)
	try
		-- Open the log file for writing, creating it if it doesn't exist
		set _log to open for access file filePath with write permission
		
		-- Construct the log entry
		set logEntry to (my formatDateTime(current date)) & " " & message & linefeed
		
		-- Write the log entry to the file
		write logEntry to _log starting at eof
		
		-- Close the log file
		close access _log
		
	on error errMsg number errNum
		-- If an error occurs, close the log file (if it's open)
		try
			close access _log
		end try
		-- Optionally, report the error in some way
		display dialog "Error: " & errMsg & " (" & errNum & ")"
	end try
end logMessage

on checkZoomRunning()
	tell application appName to activate
	set appVersion to version of application appName
end checkZoomRunning

on startParticipantWindow()
	-- We deliberately close and start the participant panel.
	tell application appName to activate
	tell application "System Events" to tell process appName
		tell menu 1 of menu bar item "View" of menu bar 1
			if exists menu item participantsClose then
				click menu item participantsClose
				my logMessage("Participants panel closed.", logFile)
				delay 1
			end if
			if exists menu item participantsOpen then
				click menu item participantsOpen
				my logMessage("Participants panel started.", logFile)
			end if
		end tell
	end tell
end startParticipantWindow

on standaloneParticipantWindow()
	tell application appName to activate
	set _return to missing value
	tell application "System Events" to tell process appName
		set _wins to windows -- The list of windows of the Zoom application
		repeat with w in _wins
			if my stringStartsWith("Participants", name of w) then
				set _return to w -- We found the free floating "Participants (NNN)" window
			end if
		end repeat
	end tell
	return _return -- This is either the handle to the window or missing value
end standaloneParticipantWindow

on checkZoomMeetingRunning()
	tell application appName to activate
	repeat
		-- Make sure we are in a Zoom meeting
		tell application "System Events" to tell process appName
			if not (exists window meetingWindow) then
				display dialog "The " & scriptName & " application needs a Zoom Meeting." & linefeed & "Please join the Zoom Meeting and press OK."
			else
				exit repeat
			end if
		end tell
	end repeat
end checkZoomMeetingRunning

on appLogMessage(message)
	my logMessage("=== " & message & " APPLICATION " & scriptName, logFile)
end appLogMessage

on writeToRoster(message, filePath)
	(*
    -- Usage:
    set logFilePath to (path to desktop as string) & "rostter.txt" -- Path to the roster file
    my writeTeRoster("John Smith", logFilePath)
    *)
	try
		-- Open the log file for writing, creating it if it doesn't exist
		set _log to open for access file filePath with write permission
		set _line to message & linefeed
		write _line to _log starting at eof
		-- Close the log file
		close access _log
	on error errMsg number errNum
		-- If an error occurs, close the log file (if it's open)
		try
			close access _log
		end try
		-- Optionally, report the error in some way
		display dialog "Error: " & errMsg & " (" & errNum & ")"
	end try
end writeToRoster

on generateRoster()
	tell application appName to activate
	tell application "System Events" to tell process appName
		set _participantWin to my standaloneParticipantWindow()
		if _participantWin is missing value then
			set _participantWin to window meetingWindow
		end if
		tell outline 1 of scroll area 1 of _participantWin
			set myParticipants to (UI elements)
			set _intro to "=== " & (my formatDateTime(current date)) & " ==="
			my writeToRoster(_intro, meetingRoster)

			set [_waiting, _joined] to [0,0] -- This is the number in Waiting Room and the numner Joined

			set _num to ((length of myParticipants) - 1)
			set _inWaitingList to false
			set _inJoinedList to false
			repeat with i from 1 to _num
				set _pName to (get value of static text of UI element of row i) as string
				if my stringStartsWith("Waiting Room ", _pName) then
					set _inWaitingList to true
				end if
				if my stringStartsWith("Joined ", _pName) then
					set _inWaitingList to false
					set _inJoinedList to true
				end if
				if (i is 1) and (not _inWaitingList) and (not _inJoinedList) then
					set _inJoinedList to true
					set _joined to 1
				end if

				set _numPrefix to ""
				if _inWaitingList and (_waiting > 0) then
					set _numPrefix to " " & (_waiting as string) & ". "
				end if
				if (not _inWaitingList) and (_joined > 0) then
					set _numPrefix to " " & (_joined as string) & ". "
				end if

				set _pName to _numPrefix & (_pName as string)
				my writeToRoster(_pName, meetingRoster)
				if _inWaitingList then
					set _waiting to _waiting + 1
				else
					set _joined to _joined + 1
				end if
			end repeat

			if _joined > 1 then
				set _joined to _joined - 1
			end if
			if _waiting > 1 then
				set _waiting to _waiting - 1
			end if
			
			set _sum to _joined + _waiting
			if _sum > 1 then
				set plural to "s"
			else
				set plural to ""
			end if
			set _summary to "=== " & (_sum as string) & " participant" & plural & " " & (my formatDateTime(current date)) & " ==="
			my writeToRoster(_summary, meetingRoster)

		end tell
	end tell
end generateRoster

on logUIHierarchy(uiElement, prefix)
	tell application "System Events"
		logMessage(prefix & " " & my UIElementToString(uiElement), logFile)
		if (exists UI elements of uiElement) then
			repeat _e in UI elements of uiElement
				logUIHierarchy(_e, "-" & prefix)
			end repeat
		end if
	end tell
end logUIHierarchy

on UIElementToString(uiElement)
	tell application "System Events"
		set resultString to ""
		set propertiesList to {"name", "title", "description", "value", "help", "class"}
		repeat with propName in propertiesList
			try
				set propValue to run script "vale of "& propName & " of " & "uiElement"
				set resultString to resultString & propName & ": " & propValue & ", "
			on error errMsg
				-- do nothing on error, so non-existing properties are ignored
			end try
		end repeat
		if resultString is not "" then
			set resultString to text 1 thru -3 of resultString -- remove the trailing comma and space
		end if
		return resultString
	end tell
end UIElementToString

-- Main logic
on main()
	my setUpFiles()
	my appLogMessage("START")
	try
		my checkZoomRunning()
		my logMessage("Zoom Version: " & appVersion, logFile)
		my checkZoomMeetingRunning()
		my startParticipantWindow()
		my generateRoster()
	on error errMsg number errNum
		set e_str to "Error: " & errMsg & " (" & errNum & ")"
		my logMessage(e_str, logFile)
		my appLogMessage("ABORT")
		display dialog e_str buttons {"Quit"}
		error e_str number errNum
	end try
	my appLogMessage("END")
end main

my main()
