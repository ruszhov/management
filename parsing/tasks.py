@shared_task(bind=True)
def prime(self, filename, cont):
    # print('s:', self)
    # print('f:', filename)
    # print('c:', cont)
    progress_recorder = ProgressRecorder(self)
    result = 0
    for i in range(2):
        time.sleep(1)
        result += i
        progress_recorder.set_progress(i + 1, 2)
    # print(progress_recorder)
    return result