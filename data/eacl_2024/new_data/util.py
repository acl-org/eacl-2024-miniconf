import math
import os
import json
import datetime
import pandas as pd
import openpyxl
import json

def str_to_date(s):
    items = s.split()
    print(items)
    month = "03"
    day = items[1].strip().strip(",")
    year = items[2].strip()
    hour = items[3].split(":")[0].strip()
    minute = items[3].split(":")[1].strip()
    datestring = "{}-{}-{} {}:{}:00".format(
        year,
        month,
        day,
        hour,
        minute
    )

    return datestring

def s2d(str):
    return datetime.datetime.strptime(str, '%Y-%m-%d').date()

def s2dt(str):
    return datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')

def s2t(str):
    return datetime.datetime.strptime(str, '%H:%M').time()

def poster_session_time(str):
    if str is None or type(str) == float:
        return ""
    def update(time):
        items = time.split(":")
        if len(items) == 1:
            # only number
            assert (items[0].strip() in ["2", "9"]), (items[0])
            if items[0].strip() == "2":
                return "14:00"
            elif items[0].strip() == "9":
                return "09:00"
        else:
            assert items[0].strip() in ["5", "12"]
            if items[0].strip() == "5":
                return "17:30"
            elif items[0].strip() == "12":
                return "12:30"

    def opt_item(item):
        start = item.split("-")[0].strip()
        end = item.split("-")[1].strip()
        start = update(start)
        end = update(end)
        return "{} - {}".format(start, end)

    items = str.split("\n")
    items = [opt_item(item) for item in items if item.strip() != ""]
    return "; ".join(items)

def prepare_tutorial_data(data_file):
    data = [
        [
            s2d("2024-03-21"), s2t("14:00"), s2t("17:30"), "Radisson", "T1", "Transformer-specific Interpretability",
            "Hosein Mohebbi, Jaap Jumelet, Michael Hanna, Afra Alishahi and Willem Zuidema",
            "tutorial-1", "Transformers have emerged as dominant players in various scientific fields, especially NLP. However, their inner workings, like many other neural networks, remain opaque. In spite of the widespread use of model-agnostic interpretability techniques, including gradient-based and occlusion-based, their shortcomings are becoming increasingly apparent for Transformer interpretation, making the field of interpretability more demanding today. In this tutorial, we will present Transformer-specific interpretability methods, a new trending approach, that make use of specific features of the Transformer architecture and are deemed more promising for understanding Transformer-based models. We start by discussing the potential pitfalls and misleading results model-agnostic approaches may produce when interpreting Transformers. Next, we discuss Transformer-specific methods, including those designed to quantify context-mixing interactions among all input pairs (as the fundamental property of the Transformer architecture) and those that combine causal methods with low-level Transformer analysis to identify particular subnetworks within a model that are responsible for specific tasks. By the end of the tutorial, we hope participants will understand the advantages (as well as current limitations) of Transformer-specific interpretability methods and how they can be applied to their own research work."
        ],
        [
            s2d("2024-03-21"), s2t("14:00"), s2t("17:30"), "Fortress 2", "T2", "LLMs for Low Resource Languages in Multilingual, Multimodal and Dialectal Settings",
            "Firoj Alam, Shammur Absar Chowdhury, Sabri Boughorbel and Maram Hasanain",
            "tutorial-2", "The recent breakthroughs in Artificial Intelligence (AI) can be attributed to the remarkable performance of Large Language Models (LLMs) across a spectrum of research areas (e.g., machine translation, question-answering, automatic speech recognition, text-to-speech generation) and application domains (e.g., business, law, healthcare, education, and psychology). The success of these LLMs largely depends on specific training techniques, most notably instruction tuning, RLHF, and subsequent prompting to achieve the desired output. As the development of such LLMs continues to increase in both closed and open settings, evaluation has become crucial for understanding their generalization capabilities across different tasks, modalities, languages, and dialects. This evaluation process is tightly coupled with prompting, which plays a key role in obtaining better outputs. There has been attempts to evaluate such models focusing on diverse tasks, languages, and dialects, which suggests that the capabilities of LLMs are still limited for medium-to-low-resource languages due to the lack of representative datasets. The tutorial offers an overview of this emerging research area. We explore the capabilities of LLMs in terms of their performance, zero- and few-shot settings, fine-tuning, instructions tuning, and close vs. open models with a special emphasis on low-resource settings. In addition to LLMs for standard NLP tasks, we will focus on speech and multimodality."
        ],
        [
            s2d("2024-03-21"), s2t("9:00"), s2t("17:30"), "Fortress 1", "T3", "Computational modeling of semantic change",
            "Pierluigi Cassotti, Francesco Periti, Stefano De Pascale, Haim Dubossarsky and Nina Tahmasebi",
            "tutorial-3", "This tutorial provides an overview of current approaches, problems and challenges in the detection of lexical semantic change. At its core, computational modelling of semantic change consists of the following: (1) Modelling word meaning, typically using unsupervised methods applied to diachronic corpora; (2) modelling meaning change, based on the results of the above; (3) evaluation. The tutorial will provide an introduction to lexical semantic change and an overview of the resources available (corpora, pre-trained diachronic models and data sets). We will highlight issues related to the creation and use of diachronic corpora and different procedures for annotating data. We will then present the current state of the art in automatic detection of LSC, provide a hands-on section on available systems and tools, and open the floor for discussion on possible applications."
        ],
        [
            s2d("2024-03-21"), s2t("9:00"), s2t("12:30"), "Fortress 2", "T4", "Item Response Theory for Natural Language Processing",
            "João Sedoc, John P. Lalor, Pedro Rodriguez and Jose Hernandez-Orallo",
            "tutorial-4", "This tutorial will introduce the NLP community to Item Response Theory (IRT). IRT is a method from the field of psychometrics for model and dataset assessment. IRT has been used for decades to build test sets for human subjects and estimate latent characteristics of dataset examples. Recently, there has been an uptick in work applying IRT to tasks in NLP. It is our goal to introduce the wider NLP community to IRT and show its benefits for a number of NLP tasks. From this tutorial, we hope to encourage wider adoption of IRT among NLP researchers.",
        ],
        [
            s2d("2024-03-21"), s2t("9:00"), s2t("12:30"), "Radisson", "T5", "Language+Molecules",
            "Carl Edwards, Qingyun Wang and Heng Ji",
            "tutorial-5", "Climate change, access to food and water, pandemics— these words, when uttered, immediately summon to mind global challenges with possible disastrous outcomes. Molecular solutions will be critical to addressing these global problems on scales of complexity never-before-seen. However, they exist in extremely large search spaces, which makes AI tools a necessity. Excitingly, the chemistry field is posed to be substantially accelerated via multimodal models combining language with molecules and drug structures."
        ]
    ]
    column_names = ['Date', 'Start Time', 'End Time', 'Room', 'Id', 'Title',
                    'Authors', 'Rocketchat', 'Desc']

    sheet_name = "Tutorials Schedule"
    # df = pd.DataFrame(
    #     data,
    #     columns=column_names
    # )
    # df.to_excel("inputs.xlsx", index=False, sheet_name="Tutorials Schedule")

    return data, column_names, sheet_name

def prepare_workshop_data(data_file):
    def _get_link_if_exists(cell):
        try:
            return cell.hyperlink.target
        except AttributeError:
            return None

    df = pd.read_excel('EACL24-Events.xlsx', sheet_name='EACL 2024 Workshops')
    ws = openpyxl.load_workbook(filename=data_file)['EACL 2024 Workshops']
    data = []
    for index, row in df.iterrows():
        if index == 0 or index > 20:
            continue

        day = row[2] # row['Day
        print(day)
        start_time = row[10] # row['Start time']
        end_time = row[15] # row['End time']
        room = "{}, {}".format(row[3], row[4]) # row['Hotel'] + ", " + row['Ballroom']
        shortname = row[8] # row['Acronym & Direct Link to Interested attendees']
        workshop_id = "Workshop-{}".format(row[7]) # + row['Wkshp #']
        title = row[9] # title
        organizers = row[38] # row['Organizer(s): First name, Last name']
        sponsors = row[29] # row['Sponsor Name(s)']
        poster_session = row[26]
        poster_session = poster_session_time(poster_session)
        desc = title
        url = _get_link_if_exists(ws.cell(row=index+2, column=10))

        data.append(
            [day.date(), start_time, end_time, room, shortname, workshop_id, title,
             organizers, poster_session, sponsors, desc, url]
        )

    column_names = ['Date', 'Start Time', 'End Time', 'Room',
                    'Shortname', 'Id', 'Title', 'organizers',
                    'Poster Session', 'Sponsors', 'Desc', 'url']

    sheet_name = "Workshop Schedule"
    df1 = pd.DataFrame(
        data,
        columns=column_names
    )
    # df1.to_excel("inputs.xlsx", index=False, sheet_name="Workshops Schedule")

    return data, column_names, sheet_name


def prepare_plenary_data(data_file):
    data = [
        [s2d("2024-03-18"), s2t("09:00"), s2t("09:30"), "Radisson",
         "EACL 2024 General Chair", "opening-session", "Opening Session and Presidential Address", "",
         "In-Person", "March 18 - Time: 09:00 - 09:30", "TBD", "EACL 2024"],
        [s2d("2024-03-18"), s2t("09:30"), s2t("10:30"), "Radisson",
         "Hongning Wang", "keynote-01", "Human vs. Generative AI in Content Creation Competition: Symbiosis or Conflict?", "",
         "In-Person", "March 18 - Time: 09:30 - 10:30", "Dr. Hongning Wang is now an associate professor at the Department of Computer Science and Technology at Tsinghua University. Prior to that, he was the Copenhaver Associate Professor in the Department of Computer Science at the University of Virginia. He received his PhD degree in computer science at the University of Illinois at Champaign-Urbana in 2014. His research generally lies in the intersection among machine learning and information retrieval, with a special focus on sequential decision optimization and computational user modeling. His work has generated over 100 research papers in top venues in data mining and information retrieval areas. He is a recipient of 2016 National Science Foundation CAREER Award, 2020 Google Faculty Research Award, and SIGIR’2019 Best Paper Award.",
         "Tsinghua University"],
        [s2d("2024-03-19"), s2t("09:00"), s2t("10:00"), "Radisson",
         "Hinrich Schütze", "keynote-02", "Quality Data for LLMs: Challenges and Opportunities for NLP", "",
         "In-Person", "March 19 - Time: 09:00 - 10:00", "Hinrich Schuetze is Professor at the Center for Information and Language Processing at LMU Munich. His lab is engaged in research on multilinguality, representation learning and linguistic analysis of NLP models. His research has been funded by NSF, the German National Science Foundation and the European Research Council (ERC Advanced Grant), inter alia. Hinrich is coauthor of two well-known textbooks (Foundations of Statistical Natural Language Processing and Introduction to Information Retrieval), a fellow of HessianAI, ELLIS (the European Laboratory for Learning and Intelligent Systems) and ACL (Association for Computational Linguistics) and (co-)awardee of several best paper awards and the ACL 2023 25-year test of time award.",
         "Ludwig Maximilian University of Munich"],
        [s2d("2024-03-19"), s2t("13:00"), s2t("13:45"), "Radisson",
         "EACL 2024 Board", "business-meeting", "Business Meeting", "",
         "In-Person", "March 19 - Time: 13:00 - 13:45", "TBD", "EACL 2024"],
        [s2d("2024-03-20"), s2t("14:45"), s2t("15:45"), "Radisson",
         "Mirella Lapata", "keynote-03", "Prompting is not all you need! Or why Structure and Representations still matter in NLP", "",
         "In-Person", "March 20 - Time: 14:45 - 15:45", "Mirella Lapata is professor of natural language processing in the School of Informatics at the University of Edinburgh. Her research focuses on getting computers to understand, reason with, and generate natural language. She is the first recipient (2009) of the British Computer Society and Information Retrieval Specialist Group (BCS/IRSG) Karen Sparck Jones award and a Fellow of the Royal Society of Edinburgh, the ACL, and Academia Europaea. Mirella has also received best paper awards in leading NLP conferences and has served on the editorial boards of the Journal of Artificial Intelligence Research, the Transactions of the ACL, and Computational Linguistics. She was president of SIGDAT (the group that organizes EMNLP) in 2018. She has been awarded an ERC consolidator grant, a Royal Society Wolfson Research Merit Award, and a UKRI Turing AI World-Leading Researcher Fellowship.",
         "University of Edinburgh"],
        [s2d("2024-03-20"), s2t("16:00"), s2t("16:45"), "Radisson",
         "EACL 2024 General Chair", "best-paper", "Best Paper Awards", "",
         "In-Person", "March 20 - Time: 16:00 - 16:45", "TBD", "EACL 2024"],
        [s2d("2024-03-20"), s2t("16:45"), s2t("17:30"), "Radisson",
         "EACL 2024 General Chair", "closing-session", "Closing Remarks & Upcoming Conference Announcements", "",
         "In-Person", "March 20 - Time: 16:45 - 17:30", "TBD", "EACL 2024"],
    ]
    column_names = ['Date', 'Start Time', 'End Time', 'Room', 'Presenter', 'id', 'Title',
                    'Session Name', 'Presentation Mode', 'Desc', 'bio', 'ins']

    sheet_name = "Plenary Schedule"
    df1 = pd.DataFrame(
        data,
        columns=column_names
    )
    # df1.to_excel("inputs.xlsx", index=False, sheet_name="Plenary Schedule")

    return data, column_names, sheet_name

def prepare_break_data(data_file):
    data = [
        ["coffee-break-1", s2d("2024-03-18"), s2t("10:30"), s2t("11:00"), "Coffee Break", "Breaks", "Coffee Break 1"],
        ["lunch-break-1", s2d("2024-03-18"), s2t("12:30"), s2t("14:00"), "Lunch Break", "Breaks", "Lunch Break 1"],
        ["coffee-break-2", s2d("2024-03-18"), s2t("15:30"), s2t("16:00"), "Coffee Break", "Breaks", "Coffee Break 2"],
        ["coffee-break-3", s2d("2024-03-19"), s2t("10:00"), s2t("10:30"), "Coffee Break", "Breaks", "Coffee Break 3"],
        ["lunch-break-2", s2d("2024-03-19"), s2t("12:00"), s2t("13:00"), "Lunch Break", "Breaks", "Lunch Break 2"],
        ["coffee-break-4", s2d("2024-03-19"), s2t("15:30"), s2t("16:00"), "Coffee Break", "Breaks", "Coffee Break 4"],
        ["coffee-break-5", s2d("2024-03-20"), s2t("10:30"), s2t("11:00"), "Coffee Break", "Breaks", "Coffee Break 5"],
        ["lunch-break-3", s2d("2024-03-20"), s2t("12:30"), s2t("14:00"), "Lunch Break", "Breaks", "Lunch Break 3"],
        ["coffee-break-6", s2d("2024-03-20"), s2t("15:45"), s2t("16:15"), "Coffee Break", "Breaks", "Coffee Break 6"],
        ["coffee-break-7", s2d("2024-03-21"), s2t("10:30"), s2t("11:00"), "Coffee Break", "Breaks", "Coffee Break 7"],
        ["lunch-break-4", s2d("2024-03-21"), s2t("12:30"), s2t("14:00"), "Lunch Break", "Breaks", "Lunch Break 4"],
        ["coffee-break-8", s2d("2024-03-21"), s2t("15:30"), s2t("16:00"), "Coffee Break", "Breaks", "Coffee Break 8"],
        ["coffee-break-9", s2d("2024-03-22"), s2t("10:30"), s2t("11:00"), "Coffee Break", "Breaks", "Coffee Break 9"],
        ["lunch-break-5", s2d("2024-03-22"), s2t("12:30"), s2t("14:00"), "Lunch Break", "Breaks", "Lunch Break 5"],
        ["coffee-break-10", s2d("2024-03-22"), s2t("15:30"), s2t("16:00"), "Coffee Break", "Breaks", "Coffee Break 10"],
    ]
    column_names = ['id', 'Date', 'Start Time', 'End Time', 'Track', 'Type', 'Session']

    sheet_name = "Breaks Schedule"
    df1 = pd.DataFrame(
        data,
        columns=column_names
    )
    # df1.to_excel("inputs.xlsx", index=False, sheet_name="Breaks Schedule")

    return data, column_names, sheet_name

def prepare_affinity_data(data_file):
    data = [
        [s2d("2024-03-19"), "13:00:00", "13:45:00", "13:00 - 13:45", "",
         "Affinity Group Meeting 1", "AGM-1", "Masakhane/Black in AI/North Africans in NLP", "", ""
         ],
        [s2d("2024-03-19"), "14:00:00", "15:30:00", "14:00 - 15:30", "",
         "Affinity Group Meeting 2", "AGM-2", "Queer in AI", "Anne Lauscher", ""
         ],
        [s2d("2024-03-20"), "11:00:00", "12:30:00", "11:00 - 12:30", "",
         "Affinity Group Meeting 3", "AGM-3", "Latin X in AI", "", ""
         ],
    ]
    column_names = ['Date', 'Start Time', 'End Time', 'Time', 'Room', 'Track', 'Session ID', 'Session Title', "Session Chairs", "Url"]
    sheet_name = "Affinity Groups & BoF"
    df1 = pd.DataFrame(
        data,
        columns=column_names
    )
    # df1.to_excel("inputs.xlsx", index=False, sheet_name="Affinity Groups & BoF")

    return data, column_names, sheet_name

def prepare_poster_data(data_file):
    def get_time(time_str):
        items = time_str.split("-")
        start_time = items[0].strip()
        return s2t("{}:00".format(start_time))

    # Oral Program Table
    df = pd.read_excel(data_file, sheet_name='PosterDemoSRWFindings Program T')
    data = []
    for index, row in df.iterrows():
        # date, Time, Paper ID, Title, Authors, Session name, Presentation Mode
        date = row['Date']
        time = row['Time CET (Local Time)']
        paper_id = row['Paper ID']
        title = row['Paper Title']
        authors = row['Authors']
        session_name = row['Conf. Session']
        presentation_mode = row['Poster Session']
        # track = row['Track']

        data.append([
            date.date(), get_time(time), paper_id, title, authors, session_name, presentation_mode
        ])
    column_names = ['Date', 'Time', 'Paper ID', 'Title', 'Authors', 'Session name', 'Presentation Mode']
    sheet_name = "PosterDemoIndustryFindings"

    df1 = pd.DataFrame(
        data,
        columns=column_names
    )
    # df1.to_excel("inputs.xlsx", index=False, sheet_name="PosterDemoIndustryFindings")

    return data, column_names, sheet_name

def prepare_oral_data(data_file):
    # Oral Program Table
    df = pd.read_excel(data_file, sheet_name='Oral Program Table')
    data = []
    for index, row in df.iterrows():
        # date, Time, Paper ID, Title, Authors, Session name, Presentation Mode
        date = row['Date']
        time = row['Time CET (Local Time)']
        room = row['Room']
        paper_id = row['Paper ID']
        title = row['Paper Title']
        authors = row['Author']
        session_name = row['Session Name ']
        presentation_mode = row['Presentation Preference']

        data.append([
            date.date(), time, room, paper_id, title, authors, session_name, presentation_mode
        ])
    column_names = ['Date', 'Time', 'Room', 'Paper ID', 'Paper Title', 'Authors', 'Session name', 'Presentation Mode']
    sheet_name = "Orals Schedule"

    df1 = pd.DataFrame(
        data,
        columns=column_names
    )
    # df1.to_excel("inputs.xlsx", index=False, sheet_name="Orals Schedule")

    return data, column_names, sheet_name

def prepare_paper_data(data_file):
    df = pd.read_excel(data_file, sheet_name='Accepted Papers')
    data = []
    for index, row in df.iterrows():
        if index <= 1:
            continue
        title = row['title']
        decision = row['decision']
        authors = row['author_names']

        data.append(
            [title, decision, authors]
        )
    column_names = ['Title', 'Decision', 'Authors']
    sheet_name = "EACL Accepted Papers"

    df1 = pd.DataFrame(
        data,
        columns=column_names
    )
    # df1.to_excel("inputs.xlsx", index=False, sheet_name="EACL Accepted Papers")

    return data, column_names, sheet_name

def write_to_excel(data_file):
    tutoral_data, tutorial_names, tutorial_sheet = prepare_tutorial_data(data_file)
    workshop_data, workshop_names, workshop_sheet = prepare_workshop_data(data_file)
    plenary_data, plenary_names, plenary_sheet = prepare_plenary_data(data_file)
    oral_data, oral_names, oral_sheet = prepare_oral_data(data_file)
    poster_data, poster_names, poster_sheet = prepare_poster_data(data_file)
    accept_data, accept_names, accept_sheet = prepare_paper_data(data_file)
    break_data, break_names, break_sheet = prepare_break_data(data_file)
    affi_data, affi_names, affi_sheet = prepare_affinity_data(data_file)

    df1 = pd.DataFrame(
        tutoral_data,
        columns=tutorial_names
    )
    df2 = pd.DataFrame(
        workshop_data,
        columns=workshop_names
    )
    df3 = pd.DataFrame(
        plenary_data,
        columns=plenary_names
    )
    df4 = pd.DataFrame(
        oral_data,
        columns=oral_names
    )
    df5 = pd.DataFrame(
        poster_data,
        columns=poster_names
    )
    df6 = pd.DataFrame(
        accept_data,
        columns=accept_names
    )
    df7 = pd.DataFrame(
        break_data,
        columns=break_names
    )
    df8 = pd.DataFrame(
        affi_data,
        columns=affi_names
    )
    writer = pd.ExcelWriter("inputs.xlsx") # , engine="xlsxwriter")
    df1.to_excel(writer, sheet_name=tutorial_sheet, index=False)
    df2.to_excel(writer, sheet_name=workshop_sheet, index=False)
    df3.to_excel(writer, sheet_name=plenary_sheet, index=False)
    df4.to_excel(writer, sheet_name=oral_sheet, index=False)
    df5.to_excel(writer, sheet_name=poster_sheet, index=False)
    df6.to_excel(writer, sheet_name=accept_sheet, index=False)
    df7.to_excel(writer, sheet_name=break_sheet, index=False)
    df8.to_excel(writer, sheet_name=affi_sheet, index=False)
    writer.close()


def convert_oral_csv(data_file):
    df = pd.read_csv(data_file, sep="\t")
    all_session, all_date, all_start_time, all_end_time = [], [], [], []
    all_location, all_track, all_pres_order, all_session_title = [], [], [], []
    all_session_id, all_pid_old, all_pid, all_title = [], [], [], []
    all_author, all_length, all_cate, all_pref = [], [], [], []
    for index, row in df.iterrows():
        # print(row.keys())
        session = row['Session']
        date = row['Date']
        start_time = row['Time CET (Local Time)']
        t_start_time = datetime.datetime.strptime(start_time, '%H:%M')
        end_time = (t_start_time + datetime.timedelta(minutes=15)).time()
        end_time = end_time.strftime('%H:%M')
        location = row['Room']
        track = row['Track'].replace("/", " ")
        presentation_order = row['Pres. Order']
        session_title = row['Session Name ']
        session_id_on_underline = ""
        pid_old = row['Paper ID'].replace(" ", "-").replace(":", "") + "-Oral"
        pid = pid_old
        title = row['Paper Title']
        author = row['Author']
        length = row['Length']
        category = row['Category']
        oral_pref = row['Presentation Preference']
        all_session.append(session.strip())
        all_date.append(date)
        all_start_time.append(start_time)
        all_end_time.append(end_time)
        all_location.append(location)
        all_track.append(track)
        all_pres_order.append(presentation_order)
        all_session_title.append(session_title)
        all_session_id.append(session_id_on_underline)
        all_pid_old.append(pid_old)
        all_pid.append(pid)
        all_title.append(title)
        all_author.append(author)
        all_length.append(length)
        all_cate.append(category.strip())
        all_pref.append(oral_pref)

    data = {
        'Session': all_session,
        'Date': all_date,
        'Start Time': all_start_time,
        'End Time': all_end_time,
        'Location': all_location,
        'Track': all_track,
        'Presentation Order': all_pres_order,
        'Session Title': all_session_title,
        'Session ID on Underline': all_session_id,
        'PID-old': all_pid_old,
        'PID': all_pid,
        'Title': all_title,
        'Author': all_author,
        'Length': all_length,
        'Category': all_cate,
        'Oral(pref)': all_pref
    }

    df1 = pd.DataFrame(data)
    df1.to_csv('oral-papers.tsv', sep="\t", index=False)


def convert_poster_csv(data_file):
    def poster_time(str):
        items =str.split("-")
        items = [item.strip() for item in items if item.strip() != ""]
        assert (len(items) == 2), (len(items))
        if ":" in items[0]:
            start_time = items[0]
        else:
            start_time = "{}:00".format(items[0])

        if ":" in items[1]:
            end_time = items[1]
        else:
            end_time = "{}:00".format(items[1])

        return start_time, end_time

    df = pd.read_csv(data_file, sep="\t")
    all_session_old, all_date, all_start_time, all_end_time = [], [], [], []
    all_pid_old, all_pid, all_title, all_author = [], [], [], []
    all_cate, all_track, all_session, all_session_id = [], [], [], []
    all_pref, all_hybrid, all_board, all_location, all_pres_order = [], [], [], [], []
    for index, row in df.iterrows():
        # print(row.keys())
        session = row['Conf. Session']
        session_old = session
        date = row['Date']
        time = row['Time CET (Local Time)']
        start_time, end_time = poster_time(time)
        pid_old = row['Paper ID'].replace(" ", "-")
        pid = pid_old
        title = row['Paper Title']
        author = row['Authors']
        if type(author) == float:
            author = row['First Authors']
        poster_session = row['Poster Session']
        if "SRW" in poster_session:
            category = "SRW"
            track = "Student Research Workshop"
            # pid += "-SRW"
            # pid_old = pid
            print(pid, "++")
        else:
            if "demo" in pid.lower():
                category = "Demo"
                track = "Demo"
            else:
                category = "Poster"
                track = row['Track'].replace("/", " ")
        session_id = ""
        poster_pref = row['Status']
        location = "Radisson"
        if "person" in poster_pref.lower():
            poster_pref = "In Person"
        elif "virtual" in poster_pref.lower():
            poster_pref = "Virtual"
            location = "GatherTown"
        hybrid = ""
        board = row['Board ']
        pres_order = ""
        all_session.append(session.strip())
        all_session_old.append(session_old.strip())
        all_date.append(date)
        all_start_time.append(start_time)
        all_end_time.append(end_time)
        all_pid_old.append(pid_old)
        all_pid.append(pid)
        all_title.append(title)
        all_author.append(author)
        all_cate.append(category)
        all_track.append(track)
        all_session_id.append(session_id)
        all_pref.append(poster_pref)
        all_hybrid.append(hybrid)
        all_board.append(board)
        all_location.append(location)
        all_pres_order.append(pres_order)

    data = {
        'Session-old': all_session_old,
        'Date': all_date,
        'Start Time': all_start_time,
        'End Time': all_end_time,
        'PID-old': all_pid_old,
        'PID': all_pid,
        'Title': all_title,
        'Author': all_author,
        'Category': all_cate,
        'Track': all_track,
        'Session': all_session,
        'Poster(pref)': all_pref,
        'Hybrid Unit No': all_hybrid,
        'Assigned Board': all_board,
        'Location': all_location,
        'Presentation Order': all_pres_order
    }

    df1 = pd.DataFrame(data)
    df1.to_csv('poster-papers.tsv', sep="\t", index=False)

def generate_plenary_json(data_file):
    df = pd.read_excel(data_file, sheet_name='Plenary Schedule')
    data = {}
    for index, row in df.iterrows():
        date = row['Date']
        bio = row['bio']
        chairs = []
        end_time = None # row['End Time']
        id = row['id']
        image_url = None
        institute = row['ins']
        link = None
        paper_ids = []
        presenter = row['Presenter']
        room = row["Room"]
        session = row['id']
        start_time = None # row['Start Time']
        title = row['Title']
        track = "Plenary"
        ttype = "Plenary Sessions"
        video_url = None
        abstract = "{} - Time: {} - {}".format(date.strftime("%A, %B %d"), row['Start Time'][:5], row['End Time'][:5])

        sample = {
            'abstract': abstract,
            'bio': bio,
            'chairs': chairs,
            'end_time': end_time,
            'id': id,
            'image_url': image_url,
            'institution': institute,
            'link': link,
            'paper_ids': paper_ids,
            'presenter': presenter,
            'room': room,
            'session': session,
            'start_time': start_time,
            'title': title,
            'track': track,
            'type': ttype,
            'video_url': video_url
        }

        data[id] = sample

    with open('plenaries.json', 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    data_file = "EACL24-Events.xlsx"
    # write_to_excel(data_file)
    convert_oral_csv("eacl-oral-papers.tsv")
    # convert_poster_csv("eacl-poster-papers.tsv")
    # generate_plenary_json("inputs.xlsx")

