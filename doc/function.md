# Function Tracking

|_exportTagSet(folderPath, banned_word)__get_banned_words("ban.txt") & get_pdf_name(folderPath)
|                                      |_get_word_list_from_file(pdf_name, banned_word)
|                                      |_get_tuned_word_list_from_folder(folderPath, banned_word)
|                                      |_break_tag_set_to_list(tag_set)
|
|_exportPDF_info(folderPath, banned_word)__get_banned_words("ban.txt") & get_pdf_name(folderPath)
|                                        |_get_word_list_from_file(pdf_name, banned_word)
|                                        |_get_page_count(pdf_name)
|_exportPDF_index(folderPath)__getpdf_name(folderPath)
|_updateStat(PDF_info.csv)__get_index_property_list(PDF_info.csv, property)
|                         |_create_characteristic_table(index_property_list)
|                         |_create_statistic_table(index_property_list)
|                         |_create_graph(index_property_list)
|                         |_export_to_dashboard(chracteristic_table, statistic_table, graph, dashboard_file)
|_exportPDF_token(PDF_info.csv)__tokenize_PDF(PDF_info.csv)
