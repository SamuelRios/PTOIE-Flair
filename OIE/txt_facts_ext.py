import csv
import argparse
from tqdm import tqdm
from OIE.predict import Predictor
from OIE.datasets.validated_splits.contractions import transform_portuguese_contractions


def main(model, input_file, output_file):
    oie = Predictor(model)
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.read()
        lines = lines.split("\n")
        
    exts = []
    lineId = 1
    for line in tqdm(lines, desc="Extraindo Informações"):
        ext = oie.pred(transform_portuguese_contractions(line), False)
        if(len(ext)> 0):
            firstExt = ext[0]
            ex = []
            ex.append(f"{lineId}")
            ex.append(line)
            ex.append(f"1.0")
            for i in firstExt:
                ex.append(i)
            exts.append(ex)
            exId = 2
            for e in ext[1:]:
                ex = []
                ex.append("")
                ex.append("")
                ex.append(f"{exId}.0")
                for i in e:
                    ex.append(i)
                exts.append(ex)
                exId += 1
        else:
            exts.append([f"{lineId}", f"{line}", "1.0"])
        lineId += 1

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';',quoting=csv.QUOTE_ALL)
        writer.writerow(['ID SENTENÇA',"SENTENÇA", "ID EXTRAÇÃO", "ARG1" , "REL" , "ARG2"])

        for ex in exts:
            lenght = len(ex)
            extraction = "extração:"
            if lenght > 5:
                writer.writerow([ex[0], ex[1], ex[2],ex[3][0], ex[4][0], ex[5][0]])
            else:
                writer.writerow([ex[0], ex[1], ex[2],"", "", ""])

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Carregar um arquivo indicado pelo usuário")
    parser.add_argument('-i', '--input', metavar='input', type=str, help='path to the input file',  required=True)
    parser.add_argument('-o', '--output', metavar='output', type=str, help='path to the output file',  default="extractedFactsByPTOIE-Flair.csv")
    parser.add_argument('-m', '--model', metavar='model', type=str, help='model',  default="TA_lsoie")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    model = args.model
    main(model=model, input_file=input_file, output_file=output_file)
    