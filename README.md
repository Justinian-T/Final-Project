Before running code ensure ffmpeg is installed, you may need to restart python or computer after downloading it and extracting the files from the zip.
You can find ffmpeg here: https://www.gyan.dev/ffmpeg/builds/

Find this: 
latest git master branch build    
version: 2025-05-01-git-707c04fe06

ffmpeg-git-essentials.7z            .ver .sha256
ffmpeg-git-full.7z                  .ver .sha256

I downloaded the full version and it works well.

Once downloaded simply extract it wherever you want
Next, go to your computer search bar and look for "edit the system environment variables"
Go to Advanced
Click "Environment Variables"
in "User variables for {User Name}" click Path and click Edit
Click Browse
Find the location you extracted ffmpeg to, click into it, click bin, and click ok. Exit out of that and restart your computer. The code will now work.

Run the app.py file, it will download all other needed dependencies
in the terminal you will see: 

Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 395-172-135

You can either paste the link into your browser or hover over the link and click it in the terminal to see the webpage it creates.