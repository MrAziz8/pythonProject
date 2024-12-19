from dataclasses import dataclass

import psycopg2


class PGConf:
    DBNAME = 'botcommerce'
    USER = 'postgres'
    PASSWORD = '1'
    HOST = 'localhost'
    PORT = '5432'
    con = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = con.cursor()


class PG(PGConf):

    def save(self):
        table_name = self.__class__.__name__.lower()
        fields = self.__dict__
        for field, value in fields.copy().items():
            if value == None:
                del fields[field]
        cols = " , ".join(fields.keys())
        format = " , ".join(["%s"] * len(fields.keys()))
        args = tuple(fields.values())
        query = f"""
            insert into {table_name} ({cols}) values ({format})
        """
        try:
            self.cur.execute(query , args)
            self.con.commit()
        except psycopg2.errors.UniqueViolation as message:
            return message

    def delete(self):
        table_name = self.__class__.__name__.lower() + "s"
        not_null_fields = self.__dict__
        [not_null_fields.pop(key) for key , value in not_null_fields.copy().items() if value == None]
        condition_format = "where " + " = %s and ".join(not_null_fields.keys()) + " = %s"
        args = tuple(not_null_fields.values())
        query = f"""
            delete from {table_name} {condition_format}
        """
        self.cur.execute(query , args)
        self.con.commit()

    def update(self , **conditions):
        table_name = self.__class__.__name__.lower() + "s"
        not_null_fields = self.__dict__
        print(not_null_fields)
        [not_null_fields.pop(key) for key , value in not_null_fields.copy().items() if value == None]
        set_format = " = %s , ".join(not_null_fields.keys()) + " = %s"
        condition_format = "where " + " = %s and ".join(conditions.keys()) + " = %s" if conditions else ""
        args = tuple(list(not_null_fields.values()) + list(conditions.values()))
        query = f"""
            update {table_name} set {set_format} {condition_format}
        """
        self.cur.execute(query , args)
        self.con.commit()

    @property
    def table_name(self):
        table_name = self.__class__.__name__.lower() + "s"
        if table_name[-2:] in ["ys"]:
            table_name = table_name[:-2] + "ies"
        return table_name

    def to_objects(self):
        columns = list(self.cur.description)
        result = self.cur.fetchall()
        results = []
        for row in result:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col.name] = row[i]
            results.append(self.__class__(**row_dict))
        return results


    def objects(self, *cols):
        table_name = self.table_name
        col_format = " , ".join(cols) if cols else "*"
        not_null_fields = self.__dict__
        [not_null_fields.pop(key) for key , value in not_null_fields.copy().items() if value == None]
        condition_format = "where " + " = %s and ".join(not_null_fields.keys()) + " = %s" if not_null_fields else ""
        args = tuple(not_null_fields.values())
        query = f"""
            select {col_format} from {table_name} {condition_format}
        """
        self.cur.execute(query , args)
        return self.to_objects()
