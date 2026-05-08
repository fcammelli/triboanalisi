import pandas as pd
import numpy as np
import os
import re
from io import StringIO
import matplotlib.pyplot as plt
import glob

def main():
    # Intestazione e sottotitolo - AGGIORNATO A 1.1.2
    header_title = "Triboanalisi 1.1.2"
    header_subtitle = "TRIBOANALISI 1.1.2 © 2025 by Francesco Cammelli is licensed under GNU GPL v3 (General Public License)"

    # Stack per gestire il back
    step_stack = []

    while True:
        print("\n" + "="*60)
        print(header_title)
        print(header_subtitle)
        print("="*60)
        print("\nQuesto programma ti permette di:")
        print("- Leggere file CSV o TXT con diversi separatori")
        print("- Selezionare colonne X e Y per l'analisi")
        print("- Riordinare i dati per valori crescenti/decrescenti")
        print("- Eliminare intervalli di dati non desiderati")
        print("- Suddividere i dati in gruppi in base a un intervallo scelto")
        print("- Visualizzare un grafico preliminare dei dati")
        print("- Calcolare medie e deviazioni standard per ogni gruppo")
        print("- Generare un nuovo file CSV con i risultati")
        print(f"- In qualsiasi momento puoi digitare 'exit' per uscire dal programma")
        print("- Oppure digitare 'back' per tornare al passaggio precedente\n")
        
        # 1. Selezione file
        current_step = "1. Selezione file"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        
        file_path = None
        while file_path is None:
            print("\nScegli come selezionare il file:")
            print("1. Scegli da un elenco di file nella cartella corrente")
            print("2. Inserisci il percorso manualmente")
            print("3. Esci dal programma")
            
            choice = input("\nInserisci il numero corrispondente alla tua scelta (1-3): ").strip().lower()
            
            if choice == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif choice == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            
            # Opzione 1: Selezione da elenco
            if choice == '1':
                # Trova tutti i file CSV e TXT nella cartella corrente ordinati alfabeticamente
                data_files = sorted(glob.glob('*.csv')) + sorted(glob.glob('*.txt'))
                
                if not data_files:
                    print("\nNessun file CSV o TXT trovato nella cartella corrente.")
                    continue
                    
                print("\nFile disponibili nella cartella corrente:")
                for i, f in enumerate(data_files, 1):
                    print(f"{i}. {f}")
                
                while True:
                    file_choice = input("\nInserisci il numero del file da analizzare (o 'back' per tornare indietro): ").strip().lower()
                    
                    if file_choice == 'exit':
                        print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                        return
                    elif file_choice == 'back':
                        break
                    
                    try:
                        file_idx = int(file_choice) - 1
                        if 0 <= file_idx < len(data_files):
                            file_path = data_files[file_idx]
                            print(f"\nFile selezionato: {file_path}")
                            break
                        else:
                            print("Numero non valido! Riprova.")
                    except ValueError:
                        print("Input non valido! Inserisci un numero.")
                if file_choice == 'back':
                    continue
            
            # Opzione 2: Inserimento manuale
            elif choice == '2':
                while True:
                    file_path = input("\nInserisci il percorso del file dati (CSV o TXT) o 'exit'/'back': ").strip()
                    if file_path.lower() == 'exit':
                        print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                        return
                    elif file_path.lower() == 'back':
                        break
                    
                    file_path = re.sub(r"^['\"]|['\"]$", '', file_path)
                    if not os.path.exists(file_path):
                        print("File non trovato! Riprova.")
                        continue
                    break
                if file_path == 'back':
                    continue
            
            # Opzione 3: Uscita
            elif choice == '3':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            
            else:
                print("Scelta non valida! Riprova.")
                continue
        
        if file_path is None or file_path == 'back':
            continue

        # 2. Selezione separatore di colonne
        current_step = "2. Selezione separatore di colonne"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        while True:
            print("\nSeleziona il separatore di colonne:")
            print("1. Virgola (CSV standard)")
            print("2. Punto e virgola")
            print("3. Tab")
            print("4. Spazio")
            sep_choice = input("Inserisci il numero corrispondente al separatore usato nel file (o 'exit'/'back'): ").strip().lower()
            
            if sep_choice == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif sep_choice == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            
            separators = {
                '1': ',',
                '2': ';',
                '3': '\t',
                '4': ' '
            }
            if sep_choice in separators:
                sep = separators[sep_choice]
                break
            else:
                print("Scelta non valida! Riprova.")
                continue
        
        if sep_choice == 'back':
            continue
        
        # 3. Lettura della prima riga (header) con il separatore scelto
        current_step = "3. Lettura dell'header del file"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            header = first_line.split(sep)
            print("\nIntestazioni delle colonne rilevate:", header)
        except Exception as e:
            print("\nErrore nella lettura dell'header del file:", e)
            if step_stack:  # Verifica se lo stack non è vuoto
                step_stack.pop()
            continue
        
        # 4. Selezione separatore di decimali
        current_step = "4. Selezione separatore di decimali"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        while True:
            decimal_sep_input = input("\nNel file i numeri decimali (ESCLUSA LA PRIMA RIGA) sono separati da '.' o ','? (digita '.' o ',' o 'exit'/'back'): ").strip().lower()
            if decimal_sep_input == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif decimal_sep_input == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            if decimal_sep_input in ['.', ',']:
                decimal_sep = decimal_sep_input
                break
            else:
                print("Input non valido! Riprova.")
                continue
        if decimal_sep_input == 'back':
            continue

        # 5. Lettura del file con i parametri selezionati
        current_step = "5. Lettura del file con i parametri selezionati"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.readlines()
            header_line = file_content[0].strip()
            header = header_line.split(sep)
            data_content = ''.join(file_content[1:])
            data_file = StringIO(data_content)
            encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    data_df = pd.read_csv(
                        data_file,
                        sep=sep,
                        engine='python',
                        encoding=encoding,
                        decimal=decimal_sep,
                        header=None
                    )
                    
                    # Gestione header mancanti
                    if len(data_df.columns) > len(header):
                        additional_cols = len(data_df.columns) - len(header)
                        for i in range(1, additional_cols + 1):
                            header.append(f"colonna incognita {len(header) + 1}")
                        print(f"\nAttenzione: Aggiunti {additional_cols} header mancanti")
                    
                    df = pd.DataFrame(data_df.values, columns=header[:len(data_df.columns)])
                    break
                except UnicodeDecodeError:
                    data_file.seek(0)
                    continue
            else:
                raise ValueError("Impossibile decodificare il file con gli encoding provati")
            data_file.seek(0)
        except Exception as e:
            print("\nErrore nella lettura del file: {}".format(e))
            print("Riprova con un separatore diverso o verifica l'encoding del file.")
            if step_stack:  # Verifica se lo stack non è vuoto
                step_stack.pop()
            continue

        # 6. Visualizzazione prime 10 righe
        current_step = "6. Visualizzazione prime 10 righe"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        print("\n" + "="*60)
        print("Anteprima delle prime 10 righe del file:")
        print(df.head(10))
        
        # 6.5 Rilevamento colonna oraria e conversione
        current_step = "6.5 Rilevamento colonna oraria e conversione"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        
        # Ricerca colonna con formato ora
        time_col = None
        time_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')
        
        for col in df.columns:
            # Controlla se almeno 5 valori nella colonna corrispondono al pattern
            time_count = df[col].astype(str).str.match(time_pattern).sum()
            if time_count > 5:  # Soglia minima per considerarla colonna oraria
                time_col = col
                print(f"\nTrovata colonna oraria: '{time_col}' con {time_count} valori nel formato HH:MM:SS")
                break
        
        if time_col:
            convert_choice = input("Vuoi convertire questa colonna in minuti decimali? (s/n): ").strip().lower()
            
            if convert_choice == 's':
                print("\nInizio conversione colonna oraria...")
                
                # Aggiunta centesimi di secondo
                time_series = df[time_col].astype(str)
                groups = time_series.groupby(time_series).groups
                
                # Crea una copia per i nuovi valori
                new_time_series = time_series.copy()
                
                # Assegna centesimi in base alla frequenza
                for time_str, indices in groups.items():
                    n = len(indices)
                    if n > 1:
                        sorted_indices = sorted(indices)
                        for i, idx in enumerate(sorted_indices):
                            centisec = round(i * (100.0 / n))
                            new_time_series[idx] = f"{time_str}:{centisec:02d}"
                
                # Normalizzazione rispetto alla prima riga
                first_time = new_time_series.iloc[0]
                parts = first_time.split(':')
                if len(parts) == 4:  # HH:MM:SS:CC
                    h1, m1, s1, c1 = map(int, parts)
                else:  # HH:MM:SS
                    h1, m1, s1 = map(int, parts)
                    c1 = 0
                
                # Funzione di conversione a minuti decimali
                def convert_to_minutes(time_str):
                    parts = time_str.split(':')
                    if len(parts) == 4:  # HH:MM:SS:CC
                        h, m, s, c = map(int, parts)
                    else:  # HH:MM:SS
                        h, m, s = map(int, parts)
                        c = 0
                    
                    # Calcolo tempo normalizzato in minuti
                    total_sec = (h - h1)*3600 + (m - m1)*60 + (s - s1) + (c - c1)/100.0
                    return round(total_sec / 60.0, 10)  # 10 cifre decimali
                
                # Applica la conversione
                df[f"{time_col}_minuti"] = new_time_series.apply(convert_to_minutes)
                
                # Passaggio E: Mostra anteprima
                print("\nAnteprima delle prime 20 righe con conversione:")
                print(df[[time_col, f"{time_col}_minuti"]].head(20))
                
                keep_choice = input("\nConfermi di voler mantenere la colonna convertita? (s/n): ").strip().lower()
                if keep_choice != 's':
                    df = df.drop(columns=[f"{time_col}_minuti"])
                    print("Conversione annullata")
                else:
                    print("Colonna convertita aggiunta con successo")
            else:
                print("Conversione saltata")
        else:
            print("\nNessuna colonna oraria rilevata. Procedo al passaggio successivo")
        
        # 7. Selezione dell'intervallo di dati da conservare
        current_step = "7. Selezione dell'intervallo di dati da conservare"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        ignore_more = None

        total_rows = len(df)
        print(f"\nIl file originale ha {total_rows} righe (da 1 a {total_rows}).")
        
        # Verifica se esiste una colonna "Label" e se ha valori validi
        has_valid_label = False
        label_mapping = ""
        if "Label" in df.columns:
            # Controlla se ci sono valori non NaN e se sono numerici/interi
            non_nan_labels = df['Label'].dropna()
            
            if len(non_nan_labels) > 0:
                # Prova a convertire in interi per verificare se sono valori interi
                try:
                    # Prova a convertire in float e poi controlla se sono interi
                    numeric_labels = pd.to_numeric(non_nan_labels, errors='coerce')
                    if not numeric_labels.isna().any():
                        # Controlla se tutti i valori sono interi
                        if (numeric_labels % 1 == 0).all():
                            has_valid_label = True
                            # Costruisci mappatura riga-label
                            int_labels = df[df['Label'].notna()].copy()
                            int_labels['Label'] = int_labels['Label'].astype(int)
                            label_mapping = "\nE' stata rilevata una colonna 'Label' con valori interi.\n"
                            label_mapping += "Le righe corrispondenti a valori interi nella colonna Label sono le seguenti:\n"
                            label_mapping += "Riga\tLabel\n"
                            label_mapping += "\n".join([f"{idx+1}\t{int(row['Label'])}" 
                                                     for idx, row in int_labels.iterrows()])
                except:
                    pass

        # SEMPRE metodo manuale
        ignore_intervals = []
        while True:
            if has_valid_label:
                print(label_mapping)
                
            ignore_more = input("\nVuoi ignorare un intervallo di righe? (s/n): ").strip().lower()
            if ignore_more == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif ignore_more == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            elif ignore_more == 'n':
                break
            elif ignore_more == 's':
                # Inserimento intervalli ripetuti
                while True:
                    print("\nInserisci l'intervallo di righe da ignorare.")
                    start_input = input("Dalla riga... (1-{} o 'ultima'): ".format(total_rows)).strip().lower()
                    if start_input == 'exit':
                        print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                        return
                    if start_input == 'back':
                        break

                    end_input = input("Alla riga... (1-{} o 'ultima'): ".format(total_rows)).strip().lower()
                    if end_input == 'exit':
                        print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                        return
                    if end_input == 'back':
                        break

                    try:
                        # Gestione "ultima"
                        start_row = total_rows if start_input == 'ultima' else int(start_input)
                        end_row = total_rows if end_input == 'ultima' else int(end_input)

                        if start_row < 1 or end_row < 1:
                            print("Inserisci numeri positivi!")
                            continue
                        if start_row > end_row:
                            start_row, end_row = end_row, start_row

                        if end_row > total_rows:
                            print(f"Attenzione: il file ha solo {total_rows} righe! Riprova.")
                            continue

                        # Aggiungi l'intervallo alla lista
                        ignore_intervals.append((start_row, end_row))
                        print(f"Intervallo aggiunto: dalla riga {start_row} alla riga {end_row}")

                        # Mostra le righe rimanenti (sempre rispetto al totale originale)
                        somma_intervalli = 0
                        for (s, e) in ignore_intervals:
                            somma_intervalli += (e - s + 1)
                        righe_rimanenti = total_rows - somma_intervalli
                        print(f"Righe rimanenti dopo aver aggiunto questo intervallo: {righe_rimanenti}")

                        # Chiedi se vogliono inserire altri
                        more = input("Vuoi inserire un altro intervallo? (s/n): ").strip().lower()
                        if more == 'exit':
                            print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                            return
                        elif more == 'n':
                            break
                    except ValueError:
                        print("Inserisci numeri interi validi o 'ultima'!")
                        continue

                # Alla fine, applica tutte le esclusioni
                if ignore_intervals:
                    mask = pd.Series([True] * len(df))
                    for (start, end) in ignore_intervals:
                        mask[(df.index >= start - 1) & (df.index <= end - 1)] = False
                    df = df[mask].reset_index(drop=True)

                    print(f"\nIntervalli ignorati: {ignore_intervals}")
                    print(f"Numero di righe rimanenti dopo l'eliminazione: {len(df)}")
            else:
                print("Risposta non valida! Riprova.")
                continue
            break

        # Controlla se dobbiamo tornare indietro
        if ignore_more == 'back':
            if step_stack:  # Verifica se lo stack non è vuoto
                step_stack.pop()
            continue

        # 8. Selezione colonne X e Y
        current_step = "8. Selezione colonne X e Y"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        print("\n" + "="*60)
        print("Seleziona le colonne per X (ascissa) e Y (ordinata):")
        print("Ecco le colonne disponibili:")
        columns = df.columns.tolist()
        for i, col in enumerate(columns, 1):
            print(f"{i}. {col}")
        
        while True:
            x_choice = input("\nInserisci il numero della colonna X (o 'exit'/'back'): ").strip().lower()
            if x_choice == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif x_choice == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            try:
                x_idx = int(x_choice) - 1
                if 0 <= x_idx < len(columns):
                    x_col = columns[x_idx]
                    break
                else:
                    print("Numero non valido! Riprova.")
            except ValueError:
                print("Inserisci un numero valido!")
        if x_choice == 'back':
            continue
        
        while True:
            y_choice = input("Inserisci il numero della colonna Y (o 'exit'/'back': ").strip().lower()
            if y_choice == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif y_choice == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            try:
                y_idx = int(y_choice) - 1
                if 0 <= y_idx < len(columns):
                    y_col = columns[y_idx]
                    break
                else:
                    print("Numero non valido! Riprova.")
            except ValueError:
                print("Inserisci un numero valido!")
        if y_choice == 'back':
            continue
        
        print("\nColonna X selezionata: '{}'".format(x_col))
        print("Colonna Y selezionata: '{}'".format(y_col))
        
        # 9. Opzione di riordino dei dati
        current_step = "9. Opzione di riordino dei dati"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        print("\n" + "="*60)
        print("Opzioni de riordino dei dati")
        while True:
            sort_choice = input("Vuoi riordinare i dati in base alla colonna X? (s/n o 'exit'/'back'): ").strip().lower()
            if sort_choice == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif sort_choice == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            elif sort_choice == 's':
                while True:
                    order_choice = input("Ordinamento crescente (c) o decrescente (d)? (c/d): ").strip().lower()
                    if order_choice == 'c':
                        df = df.sort_values(by=x_col, ascending=True)
                        print("Dati ordinati in ordine CRESCENTE per la colonna X")
                        break
                    elif order_choice == 'd':
                        df = df.sort_values(by=x_col, ascending=False)
                        print("Dati ordinati in ordine DECRESCENTE per la colonna X")
                        break
                    else:
                        print("Scelta non valida! Usa 'c' o 'd'")
                break
            elif sort_choice == 'n':
                print("Mantenuto l'ordinamento originale dei dati")
                break
            else:
                print("Scelta non valida! Riprova.")
        if sort_choice == 'back':
            continue
        
        # 9.5 Opzione di eliminazione dati
        current_step = "9.5 Opzione di eliminazione dati"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        print("\n" + "="*60)
        print("Opzioni di eliminazione dati")
        while True:
            # Visualizzazione grafica aggiornata
            plt.figure(figsize=(10, 6))
            plt.scatter(df[x_col], df[y_col], color='blue', alpha=0.5)
            plt.title("Distribuzione corrente dei dati (X-Y)")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.grid(True)
            plt.show()
            
            delete_choice = input("Vuoi eliminare un intervallo di dati? (s/n o 'exit'/'back'): ").strip().lower()
            if delete_choice == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif delete_choice == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            elif delete_choice == 'n':
                print("Mantenuti tutti i dati")
                break
            elif delete_choice == 's':
                while True:
                    try:
                        print(f"\nValori attuali della colonna X: da {df[x_col].min()} a {df[x_col].max()}")
                        x_min_del = float(input("Inserisci il valore MINIMO dell'intervallo da eliminare: ").strip())
                        x_max_del = float(input("Inserisci il valore MASSIMO dell'intervallo da eliminare: ").strip())
                        if x_min_del > x_max_del:
                            x_min_del, x_max_del = x_max_del, x_min_del
                            print("Hai inserito i valori in ordine inverso, ho corretto automaticamente")
                        # Crea una maschera per i dati da mantenere
                        mask = ~((df[x_col] >= x_min_del) & (df[x_col] <= x_max_del))
                        n_deleted = len(df) - mask.sum()
                        if n_deleted == 0:
                            print("Attenzione: nessun dato trovato nell'intervallo specificato!")
                            continue
                        print(f"Verranno eliminati {n_deleted} punti dati tra {x_min_del} e {x_max_del}")
                        confirm = input("Confermi l'eliminazione? (s/n): ").strip().lower()
                        if confirm == 's':
                            df = df[mask].reset_index(drop=True)
                            print(f"Eliminati {n_deleted} punti dati. Dati rimanenti: {len(df)}")
                            print(f"Numero di righe rimanenti: {len(df)}")
                            break
                        else:
                            print("Eliminazione annullata")
                            break
                    except ValueError:
                        print("Inserisci valori numerici validi!")
                        continue
            else:
                print("Scelta non valida! Riprova.")
        if delete_choice == 'back':
            continue

        # 9.6 - Reset delle ascisse - NUOVA FUNZIONALITÀ
        current_step = "9.6 - Reset delle ascisse"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        
        # Mostra il valore iniziale e finale delle ascisse
        x_min = df[x_col].min()
        x_max = df[x_col].max()
        print(f"\nValore iniziale delle ascisse (min): {x_min}")
        print(f"Valore finale delle ascisse (max): {x_max}")
        
        while True:
            reset_choice = input("\nVuoi azzerare il valore iniziale e normalizzare i valori delle ascisse? (s/n o 'exit'/'back'): ").strip().lower()
            if reset_choice == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif reset_choice == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            elif reset_choice == 's':
                # Azzera il valore iniziale e normalizza tutti i valori
                first_value = df[x_col].iloc[0]
                df[x_col] = df[x_col] - first_value
                
                print(f"\nNormalizzazione effettuata:")
                print(f"Primo valore ascisse normalizzato: {df[x_col].iloc[0]}")
                print(f"Ultimo valore ascisse normalizzato: {df[x_col].iloc[-1]}")
                break
            elif reset_choice == 'n':
                print("Normalizzazione non effettuata.")
                break
            else:
                print("Scelta non valida! Riprova.")
        
        if reset_choice == 'back':
            continue

        # 10. Suddivisione in gruppi - MODIFICATO PER PERMETTERE BYPASS
        current_step = "10. Suddivisione in gruppi"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        print("\n" + "="*60)
        print("Definizione degli intervalli di gruppo")
        print("Inserisci l'ampiezza dell'intervallo per suddividere i dati in gruppi.")
        print("Il programma calcolerà per ogni gruppo:")
        print("- Media dei valori X (X_mean)")
        print("- Deviazione standard dei valori X (deltaX)")
        print("- Media dei valori Y (Y_mean)")
        print("- Deviazione standard dei valori Y (deltaY)")
        print("\nEsempi di valori: 20.0, 10.0, 65.7")
        
        # Chiedi all'utente se vuole eseguire la suddivisione in gruppi
        while True:
            group_choice = input("\nVuoi eseguire la suddivisione in gruppi? (s/n o 'exit'/'back'): ").strip().lower()
            if group_choice == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif group_choice == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            elif group_choice == 'n':
                print("Suddivisione in gruppi saltata. Procedo al passaggio successivo.")
                # Crea un dataframe stats con i dati originali per compatibilità
                stats = pd.DataFrame()
                stats['intervallo'] = [f"{val:.1f}" for val in df[x_col]]
                stats['X'] = df[x_col]
                stats['deltaX'] = 0.0  # Deviazione standard zero per singoli punti
                stats['Y'] = df[y_col]
                stats['deltaY'] = 0.0  # Deviazione standard zero per singoli punti
                break
            elif group_choice == 's':
                # Procedi con la suddivisione in gruppi originale
                while True:
                    group_size_input = input("\nInserisci l'ampiezza dell'intervallo o 'exit'/'back': ").strip().lower()
                    if group_size_input == 'exit':
                        print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                        return
                    elif group_size_input == 'back':
                        break
                    try:
                        group_size = float(group_size_input)
                        if group_size <= 0:
                            print("L'ampiezza deve essere un numero positivo!")
                            continue
                        break
                    except ValueError:
                        print("Inserisci un numero valido!")
                
                if group_size_input == 'back':
                    continue
                
                x_min = df[x_col].min()
                x_max = df[x_col].max()
                print("\nIntervallo totale della colonna '{}': da {} a {}".format(x_col, x_min, x_max))
                
                # Creazione dei gruppi
                bins = np.arange(x_min, x_max + group_size, group_size)
                df['gruppo'] = pd.cut(df[x_col], bins=bins, right=False)
                
                # Calcolo statistiche per gruppo
                stats = df.groupby('gruppo').agg(
                    X_mean=(x_col, 'mean'),
                    deltaX=(x_col, 'std'),
                    Y_mean=(y_col, 'mean'),
                    deltaY=(y_col, 'std')
                ).reset_index()
                
                # Formattazione dell'intervallo
                stats['intervallo'] = stats['gruppo'].apply(lambda x: "{:.1f} - {:.1f}".format(x.left, x.right))
                stats = stats[['intervallo', 'X_mean', 'deltaX', 'Y_mean', 'deltaY']]
                stats.columns = ['intervallo', 'X', 'deltaX', 'Y', 'deltaY']
                
                # Informazioni sui gruppi
                n_groups = len(stats)
                print("\nNumero totale di gruppi creati: {}".format(n_groups))
                print("Ogni gruppo ha un'ampiezza di {}".format(group_size))
                
                # Controllo eventuali resti
                resto = len(df) - df.groupby('gruppo').size().sum()
                if resto != 0:
                    print("Attenzione: alcuni dati non rientrano perfettamente nei gruppi (resto: {} punti)".format(resto))
                
                # Visualizzazione grafica dopo la suddivisione in gruppi
                current_step = "Visualizzazione grafica dopo la suddivisione"
                print(f"\n=== {current_step} ===")
                step_stack.append(current_step)
                plt.figure(figsize=(10, 6))
                plt.scatter(df[x_col], df[y_col], color='blue', alpha=0.5, label='Dati originali')
                plt.scatter(stats['X'], stats['Y'], color='red', s=100, label='Medie dei gruppi')
                plt.title("Distribuzione dei dati e medie dei gruppi")
                plt.xlabel(x_col)
                plt.ylabel(y_col)
                plt.legend()
                plt.grid(True)
                plt.show()
                step_stack.pop()
                break
            else:
                print("Scelta non valida! Riprova.")
        
        if group_choice == 'back':
            continue
        
        # 11. Gestione righe vuote e salvataggio
        current_step = "11. Gestione righe vuote e salvataggio"
        print(f"\n=== {current_step} ===")
        step_stack.append(current_step)
        
        # Mostra anteprima prima della pulizia
        print("\nAnteprima delle prime 10 righe prima della pulizia:")
        print(stats.head(10))
        
        # Chiedi all'utente se vuole eliminare righe con valori vuoti
        while True:
            clean_choice = input("\nVuoi eliminare le righe con valori vuoti (NaN) nelle colonne X e Y? (s/n): ").strip().lower()
            if clean_choice in ['s', 'si', 'sì', 'y', 'yes']:
                original_rows = len(stats)
                # Elimina solo le righe con valori NaN nelle colonne X e Y
                stats_clean = stats.dropna(subset=['X', 'Y'])
                cleaned_rows = len(stats_clean)
                removed_rows = original_rows - cleaned_rows
                
                print(f"\nRighe prima della pulizia: {original_rows}")
                print(f"Righe dopo la pulizia: {cleaned_rows}")
                print(f"Righe rimosse: {removed_rows}")
                
                # Mostra anteprima dopo la pulizia
                print("\nAnteprima delle prime 10 righe dopo la pulizia:")
                print(stats_clean.head(10))
                
                # Chiedi conferma per usare i dati puliti
                confirm = input("\nConfermi di voler procedere con i dati puliti? (s/n): ").strip().lower()
                if confirm in ['s', 'si', 'sì', 'y', 'yes']:
                    stats = stats_clean
                    break
                else:
                    print("Pulizia annullata, verranno mantenuti tutti i dati.")
                    break
            elif clean_choice in ['n', 'no']:
                print("Operazione de pulizia annullata.")
                break
            else:
                print("Risposta non valida! Rispondi 's' o 'n'.")
        
        # Salvataggio del file CSV
        while True:
            output_filename = input("\nInserisci il nome del file CSV di output (senza estensione) o 'exit'/'back': ").strip()
            if output_filename.lower() == 'exit':
                print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
                return
            elif output_filename.lower() == 'back':
                if step_stack:  # Verifica se lo stack non è vuoto
                    step_stack.pop()
                break
            
            output_filename += ".csv"
            try:
                stats.to_csv(output_filename, index=False, sep=',')
                print("\nFile '{}' salvato con successo!".format(output_filename))
                
                # Mostra percorso completo del file salvato
                full_path = os.path.abspath(output_filename)
                print("Percorso completo del file:", full_path)
                break
            except Exception as e:
                print("Errore durante il salvataggio del file: {}".format(e))
                continue
        
        # 12. Scelta di uscita o continuazione
        print("\n" + "="*60)
        choice = input("Vuoi eseguire un'altra analisi? (s/n): ").strip().lower()
        if choice != 's':
            print("\nGrazie per aver usato {}! Arrivederci.\n".format(header_title))
            return

if __name__ == "__main__":
    main() 
