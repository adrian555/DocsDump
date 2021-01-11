* install `sleepwatcher`
  ```shell
  brew install sleepwatcher
  ```
* create `~/.sleep` and/or `~/.wakeup` file
  ```shell
  #!/bin/bash
  hour=`date +"%H"`
  if [ $hour -lt 8 ]
  then
    osascript -e 'tell app "System Events" to display dialog "Too early, go back to sleep!"'
    pmset displaysleepnow
  fi
  ```

* change the file mode
  ```shell
  chmod 700 ~/.wakeup
  chmod 700 ~/.sleep
  ```

* set up the launch agent
  ```shell
  ln -sfv /usr/local/Cellar/sleepwatcher/2.2.1/de.bernhard-baehr.sleepwatcher-20compatibility-localuser.plist ~/Library/LaunchAgents
  lanchctl load ~/Library/LaunchAgents/de.bernhard-baehr.sleepwatcher-20compatibility-localuser.plist
  ```

* remove the launch agent (optional)
  ```shell
  launchctl list |grep sleepwatcher
  launchctl remove de.bernhard-baehr.sleepwatcher
  ```
