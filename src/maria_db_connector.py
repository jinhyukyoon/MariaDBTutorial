import sys
import mariadb


class MariaDB:
    def __init__(self):
        self._initialized = False
        self._conn = None

    def __del__(self):
        if self._conn is not None:
            self._conn.cursor().close()
            self._conn.close()

    def is_initialized(self):
        return self._initialized

    def set_initialized(self, boolean: bool):
        self._initialized = boolean

    def initialize_connection(self, host: str, user: str, passwd: str, port: int = -1):
        try:
            if port < 0:
                self._conn = mariadb.connect(user=user, password=passwd, host=host)
            else:
                self._conn = mariadb.connect(user=user, password=passwd, host=host, port=port)

            self._initialized = True
        except mariadb.Error as e:
            print(f">> Error during connecting to MariaDB Platform: {e}")

    def execute_query(self, query: str):
        if self._initialized:
            try:
                cur = self._conn.cursor()
                cur.execute(query)
                self._conn.commit()

                if cur.description is not None:
                    rows = cur.fetchall()
                    print(rows, '\n')

            except mariadb.Error as e:
                print(f">> Error during executing query: {e}")


if __name__ == '__main__':
    maria = MariaDB()

    while True:
        if not maria.is_initialized():
            print('>> Enter host, user, password, port(if exists). X to exit')
        else:
            print('>> Enter query. X to exit')

        line = sys.stdin.readline().strip()
        print('')

        if len(line) == 1 and line == 'X':
            break

        if not maria.is_initialized():
            words = line.split(' ')
            if len(words) == 3:
                maria.initialize_connection(words[0], words[1], words[2])
            else:
                maria.initialize_connection(words[0], words[1], words[2], int(words[3]))

        else:
            maria.execute_query(line)
