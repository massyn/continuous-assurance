import argparse
import json
import os
import random

def generate(file,total,threshold,mappings = [ 'unknown']):
    metric = []

    for i in range(0,total):
        metric.append({
            'resource'      : f"Resource id {i+1}",
            'compliance'    : 1 if random.random() < float(threshold) else 0,
            'mapping'       : random.choice(mappings),
            'detail'        : f"Some other detail about resource {i+1}"
        })

    path = os.path.dirname(file)
    if not os.path.exists(path):
        print(f' - creating {path}')
        os.makedirs(path)

    with open(file,'wt') as q:
        q.write(json.dumps(metric,indent=2))

def main():
    parser = argparse.ArgumentParser(description='Dummy Metric generator')
    parser.add_argument('-out', help='Path to the output metric file', required=True)
    parser.add_argument('-total',help='The total number of resources that should be generated',default=100)
    parser.add_argument('-threshold',help='The random value to use to determine compliance',default=0.9)
    parser.add_argument('-mappings',help='The list of random mappings to allocate',nargs='+')

    args = parser.parse_args()

    generate(args.out,args.total,args.threshold,args.mappings)

if __name__ == '__main__':
    main()