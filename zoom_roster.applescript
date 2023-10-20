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

-- Global properties
property scriptName : "Zoom Roster"
property appName : "zoom.us"
property appVersion : missing value
property topZoomWindow : "Zoom"
property meetingWindow : "Zoom Meeting"
property sharingWindow : "zoom share statusbar window"
property participantWindow : missing value

-- These two files are created in the logs/ subdirectory of the directory where the script is run.
-- The pattern of filenames: logs/20231014-log.txt and logs/20231014-roster.txt
-- This makes it easy to store and index the logs at a later time.
property logFile : "log.txt"
property meetingRoster : "roster.txt"

on todayYMD()
	-- Return the current date in the format YYYYMMDD.
	set [_day, _month, _year] to [day, month, year] of (current date)
	set _month to _month * 1 --> 3
	set _month to text -1 thru -2 of ("0" & _month) --> "03"
	set _day to text -1 thru -2 of ("0" & _day)
	set result to _year & _month & _day
	return result
end todayYMD

on setUpFiles()
	-- setUpFiles handler:
	-- Creates a folder called "logs" in the same directory as the program if it does not already exist.
	-- It then creates two files, logFile and meetingRoster, in the logs folder, with a prefix of the current date.
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
end setUpFiles

on formatDateTime(theDateTime)
	(*
	This code takes a date and time as input and formats it into a string in the form of MM/DD/YYYY HH:MM:SS.
	It does this by extracting the day, month, year, hours, minutes, and seconds from the input and
	adding a leading zero if necessary.
	*)
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
	-- Usage:
	-- set logFilePath to (path to desktop as string) & "logfile.txt" -- Path to the log file
	-- my logMessage("This is a log message.", logFilePath)
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

on clickZoomManageParticipants()
	(*
	This code is used to click the "Manage Participants" menu item of the status menu bar.
	A delay of 1 second is added after the click.
	*)
	tell application "System Events" to tell process appName
		set menuItems to every menu item of menu 1 of menu bar 2
		repeat with m in menuItems
			if name of m starts with "Manage Participants" then
				click m
				delay 1
				my logMessage("Participants panel started.", logFile)
				exit repeat
			end if
		end repeat
	end tell
end clickZoomManageParticipants

on findParticipantsWindow()
	tell application "System Events" to tell process appName
		if exists scroll area 1 of window meetingWindow then
			set participantWindow to window meetingWindow -- Participants panel.
		else
			set _zoomWins to windows
			repeat with w in _zoomWins
				if name of w starts with "Participants" then
					set participantWindow to w -- there is a standalone Participants window
					exit repeat
				end if
			end repeat
		end if
	end tell
end findParticipantsWindow

on startParticipantWindow()
	tell application appName to activate
	tell application "System Events" to tell process appName
		my findParticipantsWindow()
		if participantWindow is missing value then
			my clickZoomManageParticipants() -- participant window started
		end if
		my findParticipantsWindow()
	end tell
end startParticipantWindow

on checkZoomMeetingRunning()
	tell application appName to activate
	repeat
		-- Make sure we are in a Zoom meeting
		tell application "System Events" to tell process appName
			set _inZoom to ((exists window meetingWindow) or (exists window sharingWindow))
			if not (_inZoom) then
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
		tell outline 1 of scroll area 1 of participantWindow
			set myParticipants to (rows)
			set _intro to "=== " & (my formatDateTime(current date)) & " ==="
			my writeToRoster(_intro, meetingRoster)
			set [_waiting, _joined] to [0, 0] -- This is the number in Waiting Room and the numner Joined
			set _num to (count myParticipants)
			set _inWaitingList to false
			set _inJoinedList to false
			repeat with i from 1 to _num
				set _pName to (get value of static text of UI element of row i) as string
				if _pName starts with "Waiting Room " then
					set _inWaitingList to true
				end if
				if _pName starts with "Joined " then
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

on letPeopleIn()
	set checkForWaitingRoom to true
	repeat while checkForWaitingRoom
		tell application "System Events" to tell process appName
			tell outline 1 of scroll area 1 of participantWindow
				-- Fetch all the rows in the Participants list.
				set participantRows to every row
				-- Check to see if Waiting Room exists.
				set firstRowName to (get value of static text of UI element of row 1) as string
				if firstRowName does not start with "Waiting Room " then
					exit repeat
				end if
				set checkForWaitingRoom to false
				-- Loop through each participant row and click the "Admit" button.
				repeat with aRow in participantRows
					if checkForWaitingRoom then
						exit repeat
					end if
					set pName to (get value of static text of UI element of aRow) as string
					if pName starts with "Joined " then
						exit repeat
					end if
					set allElem to UI elements of (item 1 of UI element of aRow)
					repeat with anElem in allElem
						if description of anElem is "Admit" then
							click anElem
							delay 1
							set checkForWaitingRoom to true
							my logMessage("Waiting Room: Admitted " & pName, logFile)
							exit repeat
						end if
					end repeat
				end repeat
			end tell
		end tell
	end repeat
end letPeopleIn

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
		my letPeopleIn()
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
