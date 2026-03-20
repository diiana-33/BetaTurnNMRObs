import argparse
import os
import pandas as pd

from glob import glob
from io import StringIO

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract dihedral angles')
    parser.add_argument('--path-to-betaturn18-outdir', default=".")
    parser.add_argument('--output-directory', default=".")
    args = parser.parse_args()

    check = True

    beta_turn_outs = glob(os.path.join(args.path_to_betaturn18_outdir, "*.out"))
    beta_turn_outs.sort()

    df_results = pd.DataFrame()
    for beta_turn_out in beta_turn_outs:
        with open(beta_turn_out, 'r') as fin:
            content = fin.read()
            if "table" not in content:
                continue
            df_tmp = pd.read_csv(StringIO("\n".join(content.split("\n")[:2])), sep=r'\s+')
            df_results = pd.concat([df_results, df_tmp])

    df_results.rename({"pdb": "time_ns"}, axis=1, inplace=True)
    for beta_turn_name, df_beta_turn in df_results.groupby("aa4"):
        df_beta_turn.to_csv(os.path.join(args.output_directory, f"{beta_turn_name}.csv"), index=False)
