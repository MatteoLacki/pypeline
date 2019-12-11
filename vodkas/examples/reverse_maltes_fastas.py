from pathlib import Path

p = Path(r'U:\Matteo\20191211_2019-015_reprocessing_with_Matteos_pipeline\20191210_up-triticum_upsp-ecoli_contaminants_T371139-E4518-C171-entries.fasta')

from furious_fastas import fastas, Fastas

FF = fastas(p)
FF.fasta_types()

FF_general = Fastas(f.to_ncbi_general() for f in FF)
FF_general.fasta_types()
FF_general.reverse()
FF_general.fasta_types()
FF_general[-1]
FF_general[1]

FF_general.write(r'X:\SYMPHONY_VODKAS\fastas\custom\Malte_fucking_big_fastas\20191210_up-triticum_upsp-ecoli_contaminants_T371139-E4518-C171-entries_with_contaminants_reverase.fasta')
