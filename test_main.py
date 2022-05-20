import subprocess

import source.process as sp
import tester

nodes_num = 6
each_times = 5

algs = ['f'] #r:RP,f:PivotRepair,p:PPT
nks = [(6, 3)]

size = 2 ** 26 #32MiB
psize =  32768 #32KiB

def main():
    t = tester.Tester(nodes_num)
    print('making executable cpp files...')
    t.make_cpp_and_send()
    print('sending config files to the nodes...')
    t.hand_out_config()
    for alg in algs:
        print('\ntesting alg:', alg)
        for n, k in nks:
            print('\nstart testing n, k: {}, {}...'.format(n, k))
            t.start_nodes(k, n - k)
            for dataset in sp.datasets:
                print('using dataset:', dataset)
                for iset, test_set in enumerate(sp.load_data(dataset, n)):
                    print('\rtesting bandwidth group: {}'.format(iset+1))
                    for ib, bw in enumerate(test_set):
                        print('\rtesting bw: {}/{}'.format(ib+1, len(test_set)), end='')
                        t.fail_node_unlimited_start(\
                            bw[:n], bw[n:-2],\
                            (\
                                (each_times, 1, (bw[-1],), (size, psize), alg),\
                            )\
                        )
                print('\rdataset {} finished\n'.format(dataset))
            print('test of n, k: {}, {} finished'.format(n, k))
            print('closing nodes...')
            t.close()
            t.wait_nodes_finish()
            cmd = 'mv files/results.txt source/new_test/results{}_{}.csv'
            subprocess.call(cmd.format(n, alg), shell=True)
        print('test of alg {} finished'.format(alg))

if __name__ == "__main__":
    main()