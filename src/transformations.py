from pyspark.sql.functions import lag
from pyspark.sql.window import Window


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
