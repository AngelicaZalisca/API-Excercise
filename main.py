
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

app = FastAPI()

api_key = "belajarapi"

@app.get("/")
def home():
    return "Selamat datang di Toko Hacktiv8!"

@app.get("/data")
def readData():
    df = pd.read_csv("dataToko.csv")
    return df.to_dict(orient='records')

@app.get("/data/{user_input}")
def searchById(user_input: int):
    df = pd.read_csv("dataToko.csv")
    filter = df[df["id"] == user_input]
    if len(filter) == 0:
        raise HTTPException(status_code=404, detail="Barang Tidak Ada")
    return filter.to_dict(orient='records')

@app.post("/item/{item_id}")
def addData(item_id: int, item_name: str, item_price: float):
    df = pd.read_csv("dataToko.csv")
    new_data = {
        "id":item_id,
        "namaBarang":item_name,
        "harga":item_price
    }

    new_df = pd.DataFrame(new_data, index=[0])

    df = pd.concat([df,new_df], ignore_index=True)
    df.to_csv("dataToko.csv", index=False)
    return f"Data dengan id {item_id} nama barang {item_name} dan harga {item_price} sudah ditambahkan"

@app.put("/update/{item_id}")
def updateData(item_id: int, item_name: str, item_price: float):
    df = pd.read_csv("dataToko.csv")
    update_data = {
        "id":item_id,
        "namaBarang":item_name,
        "harga":item_price
    }
    if update_data["id"] not in df["id"].values:
        return "Data dengan id {item_id} tidak ditemukan"
    df.loc[df["id"]==update_data["id"], "namaBarang"] = update_data["namaBarang"]
    df.loc[df["id"]==update_data["id"], "harga"] = update_data["harga"]
    df.to_csv("dataToko.csv", index=False)

    return "Barang dengan id {item_id} nama barang {item_name} sudah terupdate"

@app.get("/income")
def readIncome(password:str=Header(None)):
    if password==None:
        raise HTTPException(status_code=401, detail="Password harus diisi")
    elif password!=api_key:
        raise HTTPException(status_code=401, detail="Anda tidak memiliki akses")
    else:
        df_income = pd.read_csv("dataIncome.csv")
        return df_income.to_dict(orient='records')

