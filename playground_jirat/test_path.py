class Video(object):
    def __init__(self,path):
        self.path = path

    def play(self):
        from os import startfile
        startfile(self.path)

class Movie_MP4(Video):
    type = "MP4"

if __name__ == "__main__":
    import time
    t1 = time.time()
    state = 0
    state_state = 0
    movie1 = Movie_MP4(r"C:\Users\JIRATNAKARIT\Downloads\Video\283.mp4")
    movie2 = Movie_MP4(r"D:\Video\AI_Teach_By_AJ_Jar\0101 - Introduction to Machine Learning.mp4")
    while True:
        t_now = time.time() - t1
        print(t_now)
        if t_now >= 3 and t_now < 10:
            if state_state == 0:
                state = 1
                state_state += 1
        elif t_now >= 10 and t_now < 15:
            if state_state == 0:
                state = 2
        elif t_now > 15:
            state = 3

        if state == 1:
            movie1.play()
        elif state == 2:
            movie2.play()
        elif state == 3:
            break
        else:
            continue


