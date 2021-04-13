# python3

from collections import namedtuple

AssignedJob = namedtuple("AssignedJob", ["worker", "started_at"])

import math

class Heap():

    def __init__(self, data):
        self.data = data
        self.swaps = []
    
    # for zero-based indexing
    # left_child of node[i] = 2i + 1
    # right child of node[i] = 2i + 2
    # parent of node[i] = round_up(i/2) - 1

    def get_parent(self, i):
        index = math.ceil(i/2) - 1
        return index if index > 0 and index < len(self.data) else i

    def get_left_child(self, i):
        index = 2*i + 1
        return index if index < len(self.data) else i

    def get_right_child(self, i):
        index = 2*i + 2
        return index if index < len(self.data) else i

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
 

    def sift_down(self, i):
        # to sift a node down in min heap, check that it is strictly greater than any of its children. If parent and child are equal, swap if child_id < parent_id (priority to first thread)

        left_child = self.get_left_child(i)
        right_child = self.get_right_child(i)
        swapped = False

        if i == left_child:
            # parent has no children
            return 
        elif i == right_child:
            # Parent only has single child
            if self.data[i].next_finish_time > self.data[left_child].next_finish_time:
                j = left_child
                swapped = True
            elif self.data[i].next_finish_time == self.data[left_child].next_finish_time:
                if self.data[i].id > self.data[left_child].id:
                    j = left_child
                    swapped = True
        else:
            
            parent_finish_time, parent_id = self.data[i].next_finish_time, self.data[i].id

            left_finish_time, left_id = self.data[left_child].next_finish_time, self.data[left_child].id

        
            right_finish_time, right_id = self.data[right_child].next_finish_time, self.data[right_child].id
                
            if parent_finish_time < left_finish_time and parent_finish_time < right_finish_time:
                # sub-tree already min-heap
                return

            if left_finish_time == right_finish_time:
                if parent_finish_time > left_finish_time:
                    # parent is greater than both children that are equal -> swap with lower id among children
                    if left_id < right_id:
                        j = left_child
                        
                    else:
                        j = right_child 
                    swapped = True

                elif parent_finish_time == left_finish_time:
                    # All finish times are equal -> choose minimum id
                    if left_id < right_id and left_id < parent_id:
                        j = left_child
                        swapped = True
                    elif right_id < left_id and right_id < parent_id:
                        j = right_child
                        swapped = True
            else:
                # children have differing values
                
                if parent_finish_time > left_finish_time:
                    j = left_child
                    if left_finish_time > right_finish_time:
                        j = right_child
                    swapped = True

                elif parent_finish_time > right_finish_time:
                    j = right_child
                    if right_finish_time > left_finish_time:
                        j = left_child
                    swapped = True


                elif parent_finish_time == left_finish_time:
                    # Case 3
                    if left_id < parent_id:
                        j = left_child
                        swapped = True
                elif parent_finish_time == right_finish_time:
                    # Case 3
                    if right_id < parent_id:
                        j = right_child
                        swapped = True

        if swapped:
            self.swap(i, j)
            self.sift_down(j)


    # to build a min heap from an array, sift down all nodes from the top to second-last layer (nodes i = n/2 to 1, n = len(array))
    def build_heap(self):
        for i in range(len(self.data)//2, -1, -1):
            self.sift_down(i)

    def getMin(self):
        return self.data[0]


class Worker():
    def __init__(self, id_, next_finish_time):
        self.id = id_
        self.next_finish_time = next_finish_time
        

# All we need to do in this task is to change the code for finding best worker given in naive solution. I implemented a binary min heap which reorders the threads (threads contain id as well nextfinishtime) according to the conditions if parent thread finish time > child finish time then swap and in case of finish time is equal then check for the id of thread if parent's id is greater than child then again swap. Only this thing is needed to pass this problem.

def assign_jobs(n_workers, jobs):
    res = []
    Q = Heap([Worker(id_=n, next_finish_time=0) for n in range(n_workers)])
    for job in jobs:
        next_worker = Q.getMin()
        res.append(AssignedJob(next_worker.id, next_worker.next_finish_time))
        next_worker.next_finish_time += job
        Q.sift_down(0)

    return res

def assign_jobs_naive(n_workers, jobs):
    # TODO: replace this code with a faster algorithm.
    result = []
    next_free_time = [0] * n_workers
    for job in jobs:
        next_worker = min(range(n_workers), key=lambda w: next_free_time[w])
        result.append(AssignedJob(next_worker, next_free_time[next_worker]))
        next_free_time[next_worker] += job

    return result

def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = assign_jobs(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)
    

    ### STRESS TEST
    # import random
    # while True:
    #     n_workers = random.randint(1,50)
    #     n_jobs = random.randint(1,100)
    #     jobs = [] #[2, 9, 10, 1, 3, 4, 9, 6, 6, 10]
    #     for n in range(n_jobs):
    #         jobs.append(random.randint(1,10))
        
    #     print('{} WORKERS'.format(n_workers))
    #     print(jobs)
    #     assigned_jobs = assign_jobs_naive(n_workers, jobs)
    #     finished_job_list = assign_jobs(n_workers, jobs)

    #     for i in range(len(assigned_jobs)):
    #         if assigned_jobs[i].worker != finished_job_list[i].worker or assigned_jobs[i].started_at != finished_job_list[i].started_at:
    #             print("INCORRECT")
    #             print("ANSWER:\n")
    #             for i in assigned_jobs:
    #                 print(i.worker, i.started_at)
    #             print("\nYOUR ANSWER:\n")
    #             for i in finished_job_list:
    #                 print(i.worker, i.started_at)
                
    #             return False

    #     print("CORRECT")
        

if __name__ == "__main__":
    main()
