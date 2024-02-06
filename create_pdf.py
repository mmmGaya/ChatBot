from fpdf import FPDF




 
def simple_table(dt_inf, num_inv, spacing=1):
    data = [['Описание груза', 'Вес', 'Габариты', 'Адресс отправки', 'Адресс получения', 'Способ оплаты'],
            ['', '', '', '', '', ''],
            ['', '', '', '',  '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ]
    
    lst_info = list(dt_inf.values())

    
    # for i in range(6):
    #     data[1][i] = lst_info[i+1]
    
    pdf = FPDF()
    pdf.add_font('Open_Sans', '', 'font/OpenSans_Condensed-Regular.ttf', uni=True)
    pdf.set_font("Open_Sans", size=12)
    pdf.add_page()

    pdf.cell(200, 30, txt=f'Накладная №{num_inv} ', ln=2, align='C')
 
    pdf.set_font("Open_Sans", size=9)
    col_width = 32
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height*spacing)
 
    pdf.output(f'invoice-{num_inv}.pdf')

simple_table({'sssqwq':'w21q1111', 'sssq4wq':'w21q1111', 'ss3sqwq':'w21q1111', 's4ssqwq':'w21q1111', 'ss33sqwq':'w21q1111', 'ssffffsqwq':'w21q1111'}, 2)