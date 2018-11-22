from pyspark.sql.functions import lag
from pyspark.sql.window import Window
from pyspark.sql.functions import lit


def lagjoin(df, col, n):
    """
    :param df: PySpark DataFrame
    :param col: The name of the column to lag
    :param n: how many instances back
    :return: 
    """
    w = Window().orderBy("timestamp")

    for i in range(1, n):
        df = df.withColumn(str(col) + '_' + str(i), lag(col, i, 0).over(w) )

    df = df.withColumnRenamed(col, col + '_0')  # denote t - 0 column
    return df

def MA(df, col, n):
    """
    :param df: PySpark DataFrame
    :param col: Base column name
    :param n: window
    :return: 
    """
    base = "MA_" + str(n)
    adder = str(col) + '_'

    all = [ adder + str(i) for i in range(n) ]
    res = df.withColumn(base, sum(df[c] for c in all) / n )

    for c in all:
        res = res.drop(c)

    return res