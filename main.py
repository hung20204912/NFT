import subprocess


scripts = [
    "1.collection/collectionOpensea.py",
    "2.contract/transformContract.py",
    "3.floor/floorPriceGold.py",
    "3.floor/priceChangeRate.py",
    "4.volume/volumeGold.py",
    "4.volume/volumeChangeRate.py",
    "5.option/numberOfSaleGold.py",
    "5.option/ownersChainbase.py",
    "5.option/rankCollectionMC.py",
    "5.option/renameFields.py"
]


for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python3", script])
    print(f"Finished running {script}\n")

print("All scripts executed.")

