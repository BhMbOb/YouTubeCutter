## YouTube Cutter
-----

This is a simple script which takes a given youtube video and some other data, and splits it into individual MP3 files containing split up songs.

The main use for this script is archiving purposes of live sets which aren't available in other formats. This will allow you to download and back up the whole set as a set of MP3 files formatted like a regular album.

Note: *I do not endorse using this script for downloading copyrighted material. It should be used purely for archiving purposes.*


## Requirements
-----

- The script requires both [Python 3](https://pip.pypa.io/en/stable/) and [Pip](https://pip.pypa.io/en/stable/) to be installed on the system


## Running
-----

Download or copy the repo locally to your machine and run the **`install.bat`** file. This will create a new virtual environment within the directory and install all of the required pip packages.

After this, follow the steps below to download:


>**Set up the metadata**

Edit the **`album_data.json`** file with all required metadata for the target songs. Below is an example of the data which is required - be sure to fill it all out.

```.json
{
    "metadata":{
        "youtube_url":"https.//youtu.be/f44U9LaDk14",
        "artist": "Damien Rice",
        "album": "Live At Rock Werchter Festival"
    },

    "songs":{
        "Cannonball":0.00,
        "Delicate":3.18,
        "Elephant":8.35,
        "9 crimes":14.55,
        "Greatest Bastard":20.00,
        "The Box":26.34,
        "I Remember":31.45,
        "My Favourite Faded Fantasy":38.00,
        "Long Long Way":44.15,
        "The Blower's Daughter":50.35,
        "Volcano":55.15,
        "It Takes a Lot To Know a Man":62.28
    }
}
```

The "Songs" section should contain key/value pairs - where key is the song name, and value is the time in minutes:seconds (Ie, 32 minutes, 40 seconds would be "32:40")

>**Run The Script**

Once the data is set up you're ready to run the **`run.bat`** file - which will download and convert all data.

>**Finding The Downloaded Data**

The data is saved to the **`downloads/album_name/..`** directory. All songs will have correct artist/album metadata, along with the correctly ordered track ordering