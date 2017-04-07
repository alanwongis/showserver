import vlc
import os
import time

curr_dir = os.path.split(os.path.abspath(__file__))[0]
music_dir = os.path.join(curr_dir, "music")


instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(os.path.join(music_dir, "Lee_Rosevere_-_06_-_Arrival.mp3"))

player.set_media(media)
player.audio_set_volume(70)

player.play()
music_length = player.get_length()
while not player.get_state() == vlc.State.Ended:
    time.sleep(1)
    t =  player.get_time()/1000.0
    print t
    

    

