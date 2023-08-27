import argparse
import json
import os
import fnmatch

def findFiles(path,filter = '*'):
    q = []
    for r, d, f in os.walk(path):
        for file in f:
            if fnmatch.fnmatch(file,filter):
                q.append(os.path.join(r, file))
    return q

def pivot(X):
    print('Pivoting...')
    P = {}
    for x in X:
        for M in ['/',x['mapping']]:
            if not M in P:
                P[M] = [ 0, 0 ]

            P[M][0] += x['compliance']
            P[M][1] += 1

    R = []
    for M in P:
        R.append({
            'mapping' : M,
            'compliance' : P[M][0] / P[M][1]
        })
    return R

def pipeline(I,O):
    print('Pipeline...')
    latest = {}
    with open(f"{O}/rollup.csv",'wt') as CSV:
        CSV.write('datestamp,metric,mapping,compliance\n')

        # == find all json files in the ingestion folder
        for F in findFiles(I,'*.json'):
            print(f"File = {F}")
            # the pipeline expects files in the format 
            # YYYY/MM/DD/metric.json
            metric = os.path.basename(F).split('.')[0]
            parts = F.replace('\\','/').split('/')
            if len(parts) >= 4:
                year = int(parts[-4])
                month = int(parts[-3])
                day = int(parts[-2])
                datestamp = f"{year:04d}-{month:02d}-{day:02d}"

                print('-------------------------------------')
                print(f"metric = {metric}")
                print(f"datestamp = {datestamp}")

                # -- read the file and create a pivot of it
                with open(F,'rt') as q:
                    data = json.load(q)

                    for p in pivot(data):
                        CSV.write(f"{datestamp},{metric},{p['mapping']},{p['compliance']}\n")
                
                    # Keep a copy of the latest files (we want this for the detail)
                    if datestamp > latest.get(metric,'2000-01-01'):
                        print(f'writing {metric} for {datestamp}')
                        latest[metric] = datestamp
                        for j in data:
                            j['datestamp'] = datestamp
                        with open(f"{O}/{metric}.json",'wt') as r:
                            r.write(json.dumps(data,indent=2))
            else:
                print('invalid file format')

def main():
    parser = argparse.ArgumentParser(description='Dummy Metric generator')
    parser.add_argument('-out', help='Path to the output data file', required=True)
    parser.add_argument('-ingest',help='Path to the ingestion folder',required=True)
    
    args = parser.parse_args()

    pipeline(args.ingest,args.out)

if __name__ == '__main__':
    main()