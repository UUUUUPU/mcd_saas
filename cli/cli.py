import argparse 
from core.parser import load_mcd
from core.transformer import transform
from core.sql_generator import generate_mysql

parser =argparse.ArgumentParser()

parser.add_argument("file")
parser.add_argiment("--sgbd")

args = parser.parse_args()

mcd = load_mcd(args.file)

tables = transform(mcd)

sql = generate_mysql(tables)

print(sql)
