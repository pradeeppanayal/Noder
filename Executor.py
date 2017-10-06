import argparse
from noder import FlowManager

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--scriptSource', default='.', help='The source folder which contains the script files')
    parser.add_argument('--executionFlow', default='None', help='The execution flow file in json format')
    args = parser.parse_args()    
    scriptSource = args.scriptSource
    executionFlow = args.executionFlow
    f = FlowManager(executionFlow,scriptSource)
    f.execute()

if __name__ == '__main__':
    main()
