import mysql.connector
from mysql.connector.connection import MySQLConnection
from t_yamlReader import getyamlkey

def create_connection() -> MySQLConnection:
    """
    Establish and return a connection to a MySQL database.

    This function retrieves the database username and password from the 'getyamlkey' function
    in the 't_yamlReader' module, and attempts to establish a connection to the 'outlookScan'
    database on the 'db' host using this information.

    Returns:
        MySQLConnection: An open connection to the database.
    """
    connection = mysql.connector.connect(
        host="db",
        user=getyamlkey('dbuser'),
        password=getyamlkey('dbpassword'),
        database="outlookScan"
    )
    return connection

# 檢查是否有重複的 ID
def check_duplicate_id(id):
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT MessageID FROM mail WHERE MessageID = %s"
    cursor.execute(query, (id,))

    result = cursor.fetchone()
    if result:
        print("ID already exists.")
        result = True
    else:
        print("ID does not exist.")
        result = False

    cursor.close()
    conn.close()
    return result

# 新增mail資料到資料庫(原本的版本)
def insert_maildata(MessageID, Subject, Received,Sender):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO mail (MessageID, Subject, Received,Sender) VALUES (%s, %s, %s, %s)"
    values = (MessageID, Subject, Received, Sender)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()

# 新增attatch資料到資料庫(原本的版本)
def insert_attData(MessageID,AttatchmentName,ID):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO attatchment (MessageID,AttatchmentName,ID) VALUES (%s,%s,%s)"
    values = (MessageID,AttatchmentName,ID)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()

# 新增attatch資料（有task的版本）到資料庫
def insert_attDataTask(MessageID,AttatchmentName,ID,TaskID):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO attatchmentTask (MessageID,AttatchmentName,ID,TaskID) VALUES (%s, %s, %s, %s)"
    values = (MessageID,AttatchmentName,ID,TaskID)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully. to attatchData")

    cursor.close()
    conn.close()

def insert_task(taskID):
    from datetime import datetime
    current_time = datetime.now()
    sql_format_time = current_time.strftime('%Y-%m-%d %H:%M:%S')


    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO task (taskID, createTime, status) VALUES (%s, %s, %s)"
    values = (taskID,sql_format_time,"creating")

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()

def insert_userTask(userID,taskID):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO user_task (userID,taskID) VALUES (%s, %s)"
    values = (userID,taskID)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()

def insert_messageTask(messageID,taskID):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO mail_task (messageID,taskID) VALUES (%s, %s)"
    values = (messageID,taskID)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()

def getMailIDbyTaskID(taskID):
    conn = create_connection()
    cursor = conn.cursor()

    # Query for task 'ttttt'
    task_query = """
        SELECT * 
        FROM mail_task 
        WHERE taskID = %s
    """
    cursor.execute(task_query, (taskID,))
    messageIDs = []
    #rows = []
    for row in cursor:
        #rows.append(row)
        messageIDs.append(row[0])
    conn.close()
    return messageIDs


def getSubjectByMailID(mailID):
    conn = create_connection()
    cursor = conn.cursor()

    # Query for task 'ttttt'
    task_query = """
        SELECT * 
        FROM mail 
        WHERE MessageID = %s
    """
    cursor.execute(task_query, (mailID,))
    #rows = []
    for row in cursor:
        #rows.append(row)
        subjects=row[1]
    conn.close()
    return subjects



def getTaskByUser(userID):
    conn = create_connection()
    cursor = conn.cursor()

    # Query for task 'ttttt'
    task_query = """
        SELECT * 
        FROM user_task 
        WHERE userID = %s
    """
    cursor.execute(task_query, (userID,))
    rows = []
    for row in cursor:
        rows.append(row)
    conn.close()
    return rows

def getTaskTIme(taskID):
    conn = create_connection()
    cursor = conn.cursor()

    # Query for task 'ttttt'
    task_query = """
        SELECT * 
        FROM task 
        WHERE TaskID = %s
    """
    cursor.execute(task_query, (taskID,))
    for row in cursor:
        result = row[1]
    conn.close()
    return result

def getFileIDByTask(taskID):
    conn = create_connection()
    cursor = conn.cursor()

    # Query for task 'ttttt'
    task_query = """
        SELECT ID, AttatchmentName, TaskID 
        FROM attatchmentTask 
        WHERE TaskID = %s
    """
    cursor.execute(task_query, (taskID,))
    rows = []
    for row in cursor:
        rows.append(row)
    conn.close()
    return rows

# 取得attatchmentTask 這個表格符合TaskID的所有內容
def getTaskData(TaskID):
    conn = create_connection()
    cursor = conn.cursor()

    # Query for task 'ttttt'
    task_query = """
        SELECT * 
        FROM attatchmentTask 
        WHERE TaskID = %s
    """
    cursor.execute(task_query, (TaskID,))
    rows = []
    for row in cursor:
        rows.append(row)
    conn.close()
    return rows

def getyaraResultByFileID(fileID):
    conn = create_connection()
    cursor = conn.cursor()
    # Query for 'isBad' = 1 and join with 'yara_result'
    is_bad_query = """
        SELECT * 
        FROM yara_result 
        WHERE ID = %s
    """
    cursor.execute(is_bad_query, (fileID,))
    rows = []
    for row in cursor:
        rows.append(row)
    conn.close()
    return rows

# 取得attatchmentTask跟yararesult JOIN的結果
def getyaraResult(taskID):
    conn = create_connection()
    cursor = conn.cursor()
    # Query for 'isBad' = 1 and join with 'yara_result'
    is_bad_query = """
        SELECT yr.* 
        FROM attatchmentTask at 
        JOIN yara_result yr ON at.ID = yr.ID 
        WHERE at.isBad = 1 AND at.TaskID = %s
    """
    cursor.execute(is_bad_query, (taskID,))
    rows = []
    for row in cursor:
        rows.append(row)
    conn.close()
    return rows

def getTaskStatus(taskID):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Query for task 'ttttt'
        task_query = """
            SELECT status 
            FROM task 
            WHERE TaskID = %s
        """
        cursor.execute(task_query, (taskID,))
        rows = []
        for row in cursor:
            rows.append(row)
        conn.close()
        return {"status":rows[0][0]}
    except IndexError:
        return {"status":"taskID not found"}

# taskID_not_found
# cannot_upload {name}
# graph_api_token_failed

# initializing
# start_uploading_file
# uploading_file_done
# success

# 更新資料
def updateIsbad(id,value):
    conn = create_connection()
    cursor = conn.cursor()

    # 更新isbad
    update_query = "UPDATE attatchment SET isBad = %s WHERE ID = %s"
    values = (value, id)
    cursor.execute(update_query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()

def updateTaskStatus(taskID,status):
    conn = create_connection()
    cursor = conn.cursor()

    # 更新isbad
    update_query = "UPDATE task SET status = %s WHERE taskID = %s"
    values = (status, taskID)
    cursor.execute(update_query, values)
    conn.commit()

    print("update task"+taskID+" to " + status)

    cursor.close()
    conn.close()

def insert_taskError(taskID,error):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO taskError (taskID,Error) VALUES (%s, %s)"
    values = (taskID,error)

    cursor.execute(query, values)
    conn.commit()

    print("Error log")

    cursor.close()
    conn.close()

# 把yara結果放進yara_result表格
def insert_scanResult(filename,match):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO yara_result (ID,yara) VALUES (%s, %s)"
    values = (filename,match)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()