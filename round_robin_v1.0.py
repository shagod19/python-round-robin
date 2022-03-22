from msilib.schema import Class
from collections import deque

class Process:
        def __init__(self, pid, arrival_time, burst_time):
            self.pid = pid                      # id cua tien trinh
            self.arrival_time = arrival_time    # thoi gian tien trinh den
            self.burst_time = burst_time        # thoi gian tien trinh thuc hien
            self.bt_remaining = burst_time      # thoi gian tien trinh con phai thuc hien la bao nhieu
            self.completion_time = 0            # moc thoi gian tien trinh chay xong
            self.turn_around_time = 0           # khoang thoi gian tu luc tien trinh den va tien trinh chay xong
            self.wait_time = 0                  # thoi gian tien trinh phai doi de thuc hien xong
            self.start_time = 0                 # moc thoi gian tien bat dau chay
        # phuong thuc de in ra cac thong tin cua tien trinh ra terminal
        def print_info(self):
                print(f"{self.pid}\t\t{self.arrival_time}\t\t\t{self.burst_time}\t\t\t{self.start_time}\t\t\t{self.completion_time}\t\t\t{self.turn_around_time}\t\t\t{self.wait_time}")
        # phuong thuc tra lai thong tin duoi dang string de luu vao file
        def return_info(self):
                string = "\n{}\t\t{}\t\t\t{}\t\t\t{}\t\t\t{}\t\t\t{}\t\t\t{}".format(self.pid,self.arrival_time,self.burst_time,self.start_time,self.completion_time,self.turn_around_time,self.wait_time)
                return string

def round_robin(pid_list,burst_time_list,arrival_time_list,quantium_list):
        queue = []                      # hang doi
        visited = []                    # list cac process check xem process da duoc them vao queue chua
        Processes = []                  # list cac process phai thuc hien
        executed_processes = []         # dung de luu lai lich su thu tu cac process da thuc hien
        completed = 0                   # bien dem de dem cac tien trinh da thuc hien xong chua
        current_time = 0                # bien thoi gian thuc
        sum_turn_around_time = 0        # tong thoi gian turn around time cua cac tien trinh
        sum_waiting_time = 0            # tong thoi gian doi cua cac tien trinh
        # them cac process vao list Processes
        for i in range(len(pid_list)):
                process = Process(pid_list[i], arrival_time_list[i], burst_time_list[i])
                Processes.append(process)
        # sap xep thu tu cac process theo thoi gian process nao den truoc
        Processes.sort(key=lambda x: x.arrival_time)
        # tao list visited danh dau tat ca cac process chua cai nao dua vao queue
        for i in range(len(Processes)):
                visited.append(False)
        # them tien trinh dau tien vao queue
        queue.append(0)
        # danh dau tien trinh dau tien da duoc them vao queue
        visited[0] = True 
        while completed != len(pid_list):
                # lay process ra khoi queue de thuc chay
                index = queue.pop(0)
                # them vao list lich su thu tu cac process da chay
                executed_processes.append(index)
                '''
                kiem tra xem process vua duoc lay ra tu queue da chay chua
                neu chua chay thi set thuoc tinh start_time
                dat current_time = starttime
                '''
                if Processes[index].bt_remaining == Processes[index].burst_time:
                        Processes[index].start_time = max(current_time, Processes[index].arrival_time)
                        current_time = Processes[index].start_time
                '''
                - neu thoi gian hoan thanh tien trinh lon quantium thi
                bt_remaing tru di va current_time cong them quantium.
                - neu thoi gian nho hon thi set bt_remaing = 0 cap nhat
                lai current_time, completion time, ... completed them 1
                don vi.
                '''
                if Processes[index].bt_remaining - quantium > 0:
                        Processes[index].bt_remaining -= quantium
                        current_time += quantium
                else:
                        current_time += Processes[index].bt_remaining
                        Processes[index].bt_remaining = 0
                        completed += 1
                        Processes[index].completion_time = current_time
                        Processes[index].turn_around_time = Processes[index].completion_time - Processes[index].arrival_time
                        Processes[index].wait_time = Processes[index].turn_around_time - Processes[index].burst_time
                        sum_turn_around_time += Processes[index].turn_around_time
                        sum_waiting_time += Processes[index].wait_time
                # kiem tra xem co tien trinh nao da den chua neu den roi them vao queue
                for i in range(1, len(Processes)):
                        if Processes[i].bt_remaining > 0 and Processes[i].arrival_time <= current_time and visited[i] == False:
                                queue.append(i)
                                visited[i] = True
                # neu process vua roi chua hoan thanh thi them vao queue
                if Processes[index].bt_remaining > 0:
                        queue.append(index)
                # neu queue rong thi kiem tra cac process co process nao chua duoc thuc hien xong khong khong thi them vao queue
                if len(queue) == 0:
                        for i in range(1, len(Processes)):
                                if Processes[i].bt_remaining > 0:
                                        queue.append(i)
                                        visited[i] = True
                                        break
        # sort lai de hien thi va ghi vao file
        Processes.sort(key=lambda x: x.arrival_time)
        print(f"PID\t\tArrival_Time\t\tBurst_Time\t\tStart_Time\t\tComplete_Time\t\tTurn_Around_time\tWait_time")
        for process in Processes:
            process.print_info()
        print(f"Average Turn Around Time: {sum_turn_around_time/len(Processes)}")
        print(f"Average Waiting Time: {sum_waiting_time/len(Processes)}")
        print(f"Executed process: {executed_processes}")
        with open("round_robin.txt", "w") as file:
                file.writelines(f"PID\t\tArrival_Time\t\tBurst_Time\t\tStart_Time\t\tComplete_Time\t\tTurn_Around_time\tWait_time")
                for process in Processes:
                        file.writelines(process.return_info())
                file.writelines(f"\nAverage Turn Around Time: {sum_turn_around_time/len(Processes)}")
                file.writelines(f"\nAverage Waiting Time: {sum_waiting_time/len(Processes)}")
            
if __name__ =="__main__":
    pid_list = [0,1,2,3,4]
    burst_time_list = [11,7,19,4,9]
    arrival_time_list = [0,3,8,13,17]
    quantium = 3
    round_robin(pid_list, burst_time_list, arrival_time_list, quantium)
    