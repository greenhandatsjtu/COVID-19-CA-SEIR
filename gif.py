from moviepy.editor import ImageSequenceClip

img_names = [str(i) + '.png' for i in range(10)]
clip = ImageSequenceClip(img_names, fps=2)
clip.write_gif('herd_immune.gif')
