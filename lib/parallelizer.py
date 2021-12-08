import logging
import multiprocessing
import time
import tiny_timer

def parallelize(func,lst,args=(),threads=2*multiprocessing.cpu_count(),
                timer_step=300,max_time_stuck=900,log_level=logging.DEBUG,
                **kwargs):
    logger=logging.getLogger('parallelize')
    logger.setLevel(log_level)
    pool=multiprocessing.Pool(processes=threads)
    output=[]
    tot=len(lst)
    timer=tiny_timer.tiny_timer(tot,timer_step=timer_step,max_time_stuck=max_time_stuck)
    for i in lst:
        pool.apply_async(func,(i,)+args,kwargs,callback=output.append)
    pool.close()
    time_stuck=0
    cnt=0
    while cnt<tot:
        seconds_left,very_stuck=timer.check_timer(cnt=cnt)
        if very_stuck:
            logger.warning('Terminating the parallelizer pool: {} out of {} tasks got stuck!'.format(tot-cnt,tot))
            pool.terminate()
            break
        time.sleep(min(timer_step,seconds_left))
        cnt=len(output)
    return output

def function_wrapper(x,wrapped_func,*args,**kwargs):
    try:
        return wrapped_func(x,*args,**kwargs)
    except:
        return False