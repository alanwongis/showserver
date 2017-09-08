import vlc
import os
import time
import threading
import queue

import inspect

curr_dir = os.path.split(os.path.abspath(__file__))[0]
music_dir = os.path.join(curr_dir, "music")
        

class VLCThread(threading.Thread):
    def __init__(self, playlist = []):
        super(VLCThread, self).__init__()
        self.daemon = True
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.cmds = queue.Queue()
        self.playlist = playlist
        self.song_index = 0
        self.song = self.playlist[0]
        self.state = "stopped"

    # public interface to control the player
    def change_song(self, track_num=None):
        """change to the given track number (1...N) """
        try:
            song_num = int(song_num)
            if song_num >=1 and (song_num-1)<len(self.playlist):
                self.cmds.put( ("change_song", song_num-1))
        except:
            print("error changing song")

    def stop(self):
        self.cmds.put( ("stop", None))

    def pause(self):
        self.cmds.put( ("pause", None))

    def next(self):
        self.cmds.put( ("next", None))

    def prev(self):
        self.cmds.put( ("prev", None))
        
    def play(self):
        """single button control-toggles between a playing/pause state"""
        self.cmds.put( ("play", None))

    def set_playlist(self, playlist):
        self.cmds.put( ("playlist", playlist))

    def get_status(self):
        if self.state == "playing" or self.state == "paused":
            time = int(self.player.get_time()/1000)
        else:
            time = 0
        length = int(self.player.get_length()/1000)
        return {"state": self.state, "track_title": self.song, "track_num": self.song_index+1, "time":time, "length": length}
        
   
    def run(self):
        running = True
        print("running thread")
        while running:
            time.sleep(0.1)
            while self.cmds.qsize() > 0:
                cmd, param = self.cmds.get()
                print("got command", cmd)
                if cmd == "playlist":
                    self.player.stop()
                    self.playlist = param
                    self.song_index = 0
                    self.song = self.playlist[self.song_index]
                    self.state = "stopped"
                    
                elif cmd == "change_song":
                    if self.state == "stopped" or self.state=="paused":
                        self.song_index = param
                        self._set_song()
                    elif self.state == "playing":
                        self.player.pause()
                        self.song_index = param
                        self._set_song()
                        self.player.play()
                        self.state = "playing"
                        
                elif cmd == "stop":
                    if self.state == "playing" or self.state=="paused":
                        self.player.stop()
                        self.song_index = 0
                        self.state = "stopped"
                        
                elif cmd == "pause":
                    if self.state == "playing":
                        self.player.pause()
                        self.state = "paused"
                    elif self.state == "paused":
                        self.player.pause()
                        self.state = "playing"
                        
                elif cmd == "play":
                    if self.state == "playing":
                        self.player.pause()
                        self.state = "paused"
                    elif self.state == "stopped":
                        self._set_song()
                        self.player.play()
                        self.state = "playing"
                    elif self.state == "paused":
                        self.player.play()
                        self.state = "playing"
                        
                elif cmd == "next":
                    if self.song_index < len(self.playlist)-1:
                        self.song_index += 1
                        if self.state == "playing":
                            self.player.stop()
                            self._set_song()
                            self.player.play()
                            self.status = "playing"
                        elif self.state == "paused":
                            self.player.stop()
                            self._set_song()
                            self.status = "stopped"
                        elif self.state == "stopped":
                            self._set_song()
                            self.state = "stopped"
            
                elif cmd == "prev":
                    if self.song_index > 0:
                        self.song_index -= 1
                        if self.state == "playing":
                            self.player.stop()
                            self._set_song()
                            self.player.play()
                            self.status = "playing"
                        elif self.state == "paused":
                            self.player.stop()
                            self._set_song()
                            self.status = "stopped"
                        elif self.state == "stopped":
                            self._set_song()
                            self.state = "stopped"
                elif cmd == "quit":
                    running = False
                    
            # advance the playlist during play            
            if self.state == "playing":
                if self.player.get_state() == vlc.State.Ended: 
                    if self.song_index < len(self.playlist)-1:
                        self.song_index += 1
                        self._set_song()
                        self.player.play()
                        
    # internal helper method
    def _set_song(self):
        self.song = self.playlist[self.song_index]
        song_path = os.path.join(music_dir, self.song)
        media = self.instance.media_new(song_path)
        self.player.set_media(media)
        
                        
        
if __name__ == "__main__":
    
    playlist = ['01 Common People.m4a', '02 Mediational Field.m4a']
    player = VLCThread(playlist)
    player.start()
    while True:
        cmd = input(">")
        if cmd == u"play":
            player.play()
        elif cmd == u"stop":
            player.stop()
        elif cmd == u"status":
            print (str( player.get_status() ))
        elif cmd == u"next":
            player.next()
        elif cmd == u"prev":
            player.prev()
        elif cmd.startswith(u"song") and  len(cmd.split(" ")) == 2:
                player.change_song(cmd.split(" ")[1])
        else:
            print("unknown command")
        if cmd == "quit":
            break
       
    print("done")
    
    #clean up the player thread
    player.running = False
    player.join(2)
    



    

