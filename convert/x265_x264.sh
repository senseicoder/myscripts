#convertir x265 to x264
#https://askubuntu.com/questions/778137/how-to-convert-a-video-file-from-mkv-to-a-format-supported-by-the-tv-set
#
#On any Ubuntu newer than that, a simple apt update followed by apt install ffmpeg will install a newer version. If you are on 14.04, add this ppa by add-apt-repository ppa:mc3man/trusty-media to get the latest ffmpeg.

for i in *.mkv ; do
    echo $i
    ffmpeg -i "$i" -bsf:v h264_mp4toannexb -sn -map 0:0 -map 0:1 -vcodec libx264 "$i.ts"
    mv "$i.ts" "$i.mpg"
    sleep 3
done
