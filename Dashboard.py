import pandas as pd
import string
import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")

# Loading Dataset yag diperlukan
df_name = ["jumlah_korban", "korban_terlayani", "tempat_kejadian", 
           "total_korban_kabupaten_kota"]
csv_list = ["jumlah_korban.csv", "korban_terlayani.csv", "tempat_kejadian.csv", 
           "total_korban_kabupaten_kota.csv"]
df = []

for i in csv_list:
    df.append(pd.read_csv(i))

# Membuat list yang akan ditampilkan pada multiselect
list_tahun = df[df_name.index("jumlah_korban")]["tahun"].unique().tolist()
list_tahun.append("2017-2021")

list_kab_kota = df[df_name.index("jumlah_korban")]["kabupaten/kota"].unique().tolist()
list_kab_kota.append("jawa barat")

# Setting layout untuk streamlit
st.caption("Capstone Project Tetris II - Iqbal M. Yusuf")
st.markdown("<h1 style='text-align: center; font-size: 44px;'>EKSPLORASI KASUS TINDAK KEKERASAN DI JAWA BARAT TAHUN 2017-2021</h1>", unsafe_allow_html=True)
# st.write("\n")
# st.markdown("<h1 style='text-align: center; font-size: 24px;'><a href='https://www.kompas.tv/article/311301/bocah-sd-dipaksa-teman-temannya-setubuhi-kucing-sambil-direkam-korban-depresi-hingga-meninggal'><i>\"Bocah SD Dipaksa Teman-temannya Setubuhi Kucing Sambil Direkam, Korban Depresi hingga Meninggal\"</i></a></h1>", unsafe_allow_html=True)
st.write("\n")

st.markdown("<p style='text-align: justify; font-size: 18px;'><i>Dashboard</i> ini berisi data hasil eksplorasi terhadap kasus tindak kekerasan yang terjadi di provinsi Jawa Barat. Adapun data yang ditampilkan berupa data jumlah kasus kekerasan, jenis kekerasan, tempat terjadinya kekerasan, dan perbandingan antara jumlah korban terlapor dengan korban terlayani yang disajikan dalam bentuk <i>line, bar,</i> dan <i>pie chart</i>.</p>", unsafe_allow_html=True)
st.write("\n")
st.write("\n")

# Inisialiasi fungsi untuk menampilkan grafik
def line_chart(data, x, y, color, colormap, title):
    fig = px.line(data, x=x, y=y, color=color, color_discrete_map=colormap, width=700, height=600)
    fig.update_layout(title={ 'text': title,
                              'y':0.97,
                              'x':0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                      title_font_size=24,
                      yaxis_title='jumlah korban')
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
    return fig

def hbar_chart(data, x, y, color, colormap, title):
    fig = px.bar(data1, x=x, y=y, color=color, color_discrete_map=colormap, width=700, height=600)
    fig.update_layout(title={ 'text': "Data Tahun {}".format(tahun),
                              'y':0.97,
                              'x':0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                      title_font_size=24,
                      xaxis_title='jumlah korban')
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
    fig.update_yaxes(categoryorder='total descending')
    return fig


def bar_chart(data, x, y, color, colormap, title):
    fig = px.bar(data, x=x, y=y, color=color, color_discrete_map=colormap, width=600, height=600)
    fig.update_layout(title={ 'text': title,
                                  'y':0.97,
                                  'x':0.5,
                                  'xanchor': 'center',
                                  'yanchor': 'top'},
                      title_font_size=24)
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
    fig.update_yaxes(title="jumlah korban")
    return fig


def pie_chart(data, value, name, color, colormap, title):
    fig = px.pie(data, values=value, names=name, color=color, color_discrete_map=colormap, width=600, height=600)
    fig.update_layout(title={ 'text': title,
                              'y':0.97,
                              'x':0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                      title_font_size=24)
    fig.add_annotation(dict(font=dict(size=20),
                            x=0.40,
                            y=-0.05,
                            showarrow=False,
                            text="Total: {}".format(sum(data[value])),
                            xanchor='left'))
    return fig

# Memasukkan data ke dashboard
with st.sidebar:
    st.header("Filter data")
    tahun = st.selectbox("Pilih tahun", list_tahun)
    kab_kota = st.selectbox("Pilih kabupaten/kota", list_kab_kota)
    korban = st.selectbox("Pilih korban", ["anak laki-laki", "anak perempuan", "perempuan", "keseluruhan"])

# Membuat grafik yang berisi data kekerasan pertahun/per-kabupaten/kota
col1, col2 = st.columns(2, gap="large")
with col2:
    tipe = st.selectbox("Pilih jenis visualisasi", ["Data per tahun", "Data per kabupaten/kota"])
    x1 = 'jumlah'
    y1 = 'kabupaten/kota'
    color1 = 'korban'
    cmap1 = {'anak_laki_laki': '#7ED0F7', 'anak_perempuan': '#D0F77E', 'perempuan' : '#F77ED0'}

    if tipe == "Data per tahun":
        title1 = "Data Tahun {}".format(tahun)

        if tahun == "2017-2021":
            data1 = df[df_name.index("total_korban_kabupaten_kota")].groupby(["kabupaten/kota", "korban"]).sum().reset_index()
            st.plotly_chart(hbar_chart(data1, x1, y1, color1, cmap1, title1))

        else:
            data1 = df[df_name.index("total_korban_kabupaten_kota")].loc[df[df_name.index("total_korban_kabupaten_kota")]["tahun"] == tahun]
            st.plotly_chart(hbar_chart(data1, x1, y1, color1, cmap1, title1))

    else:
        x1 = 'tahun'
        y1 = 'jumlah'
        title1 = "Jumlah Kekerasan di {}".format(string.capwords(kab_kota))

        if kab_kota == "jawa barat":
            data1 = df[df_name.index("total_korban_kabupaten_kota")].groupby(["tahun", "korban"]).sum().reset_index()
            data1["tahun"] = data1["tahun"].astype(str)
            st.plotly_chart(line_chart(data1, x1, y1, color1, cmap1, title1))

        else:
            data1 = df[df_name.index("total_korban_kabupaten_kota")].loc[df[df_name.index("total_korban_kabupaten_kota")]["kabupaten/kota"] == kab_kota]
            data1["tahun"] = data1["tahun"].astype(str)
            st.plotly_chart(line_chart(data1, x1, y1, color1, cmap1, title1))

with col1:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.markdown("<h1 style='text-align: left; font-size: 32px;'>Berapa banyak kasus kekerasan yang terjadi?", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; font-size:18px;'>Dari visualisasi disamping, dapat dilihat bahwa terjadi kenaikan kasus tindak kekerasan dari tahun 2018-2019 dan 2020-2021 dengan Kota Bandung sebagai kota dengan jumlah kasus tindak kekerasan yang paling tinggi.</p>", unsafe_allow_html=True)   

# Membuat section untuk grafik baru
st.write("\n")
st.write("\n")
col1, col2 = st.columns(2, gap="large")

# Membuat grafik yang berisi jenis kekerasan yang dialami oleh korban
with col1:
    st.markdown("<h1 style='text-align: left; font-size: 32px;'>Kekerasan apa saja yang dialami oleh korban {} di {} ?</h1>".format(korban, string.capwords(kab_kota)), unsafe_allow_html=True)
    
    x2 = 'tahun'
    color2 = 'jenis_kekerasan'
    cmap2 = {"eksploitasi": "#ADADAD", "fisik": "#7ED0F7", "lainnya": "#7E94F7", "penelantaran": "#F77ED0", "psikis": "#F77E94", "seksual": "#D0F77E", "trafficking": "#94F77E"}
    title2 = 'Jenis Kekerasan'

    if kab_kota == "jawa barat":
        if korban == "anak laki-laki":
            y2 = 'jumlah_korban_anak_laki-laki'
            data2 = df[df_name.index("jumlah_korban")].groupby(["tahun", "jenis_kekerasan"])["jumlah_korban_anak_laki-laki"].sum().reset_index()
            st.plotly_chart(bar_chart(data2, x2, y2, color2, cmap2, title2))

        elif korban == "anak perempuan":
            y2 = 'jumlah_korban_anak_perempuan'
            data2 = df[df_name.index("jumlah_korban")].groupby(["tahun", "jenis_kekerasan"])["jumlah_korban_anak_perempuan"].sum().reset_index()
            st.plotly_chart(bar_chart(data2, x2, y2, color2, cmap2, title2))

        elif korban == "perempuan":
            y2 = 'jumlah_korban_perempuan'
            data2 = df[df_name.index("jumlah_korban")].groupby(["tahun", "jenis_kekerasan"])["jumlah_korban_perempuan"].sum().reset_index()
            st.plotly_chart(bar_chart(data2, x2, y2, color2, cmap2, title2))
        
        else:
            y2 = 'keseluruhan'
            data2 = df[df_name.index("jumlah_korban")].groupby(["tahun", "jenis_kekerasan"]).sum().reset_index()
            data2["keseluruhan"] = data2["jumlah_korban_anak_laki-laki"] + data2["jumlah_korban_anak_perempuan"] + data2["jumlah_korban_perempuan"]
            st.plotly_chart(bar_chart(data2, x2, y2, color2, cmap2, title2))

    else:
        if korban == "anak laki-laki":
            y2 = 'jumlah_korban_anak_laki-laki'
            data2 = df[df_name.index("jumlah_korban")].loc[df[df_name.index("jumlah_korban")]["kabupaten/kota"] == kab_kota]
            st.plotly_chart(bar_chart(data2, x2, y2, color2, cmap2, title2))

        elif korban == "anak perempuan":
            y2 = 'jumlah_korban_anak_perempuan'
            data2 = df[df_name.index("jumlah_korban")].loc[df[df_name.index("jumlah_korban")]["kabupaten/kota"] == kab_kota]
            st.plotly_chart(bar_chart(data2, x2, y2, color2, cmap2, title2))

        elif korban == "perempuan":
            y2 = 'jumlah_korban_perempuan'
            data2 = df[df_name.index("jumlah_korban")].loc[df[df_name.index("jumlah_korban")]["kabupaten/kota"] == kab_kota]
            st.plotly_chart(bar_chart(data2, x2, y2, color2, cmap2, title2))
        
        else:
            y2 = 'keseluruhan'
            data2 = df[df_name.index("jumlah_korban")].loc[df[df_name.index("jumlah_korban")]["kabupaten/kota"] == kab_kota]
            data2 = data2.groupby(["tahun", "jenis_kekerasan"]).sum().reset_index()
            data2["keseluruhan"] = data2["jumlah_korban_anak_laki-laki"] + data2["jumlah_korban_anak_perempuan"] + data2["jumlah_korban_perempuan"]
            st.plotly_chart(bar_chart(data2, x2, y2, color2, cmap2, title2))

    st.markdown("<p style='text-align: justify; font-size: 18px;'>Jenis kekerasan yang sering terjadi adalah kekerasan seksual, fisik, dan psikis. Untuk korban anak laki-laki dan anak perempuan, jenis kekerasan yang paling sering terjadi (besar proporsinya) adalah kekerasan seksual sementara untuk perempuan umumnya berupa kekerasan psikis.</p>", unsafe_allow_html=True)

# Grafik tempat terjadinya tindak kekerasan
with col2:
    st.markdown("<h1 style='text-align: left; font-size: 32px;'>Lalu, untuk {}, tindak kekerasan tersebut sering terjadi di mana?</h1>".format(string.capwords(kab_kota)), unsafe_allow_html=True)
    
    x3 = 'tahun'
    y3 = 'jumlah_kekerasan'
    color3 = 'tempat_kejadian'
    cmap3 = {"rumah tangga": "#D77EF7", "tempat kerja": "#7EF79A", "lainnya": "#F79A7E", "sekolah": "#F7D77E", "fasilitas umum": "#7EF7D7", "lembaga pendidikan kilat": "#9A7EF7"}
    title3 = 'Tempat Kejadian Kekerasan'

    if kab_kota == "jawa barat":
        data3 = df[df_name.index("tempat_kejadian")].groupby(["tahun", "tempat_kejadian"])["jumlah_kekerasan"].sum().reset_index()
        st.plotly_chart(bar_chart(data3, x3, y3, color3, cmap3, title3))

    else:
        data3 = df[df_name.index("tempat_kejadian")].loc[df[df_name.index("tempat_kejadian")]["kabupaten/kota"] == kab_kota]
        st.plotly_chart(bar_chart(data3, x3, y3, color3, cmap3, title3))

    st.markdown("<p style='text-align: justify; font-size: 18px;'>Berdasarkan grafik, kekerasan sering terjadi di rumah, fasilitas umum, sekolah dan lainnya (diluar kategori yang ada pada grafik). Dari grafik jenis kekerasan, dapat dilihat bahwa kekerasan yang terjadi dapat dikaitkan dengan adanya permasalahan dalam keluarga yang berujung pada kekerasan psikis dan fisik.</p>", unsafe_allow_html=True)

# Membuat section yang membandingkan antara kasus yang terlapor dan kasus yang terlayani
st.write("\n")
st.write("\n")
st.markdown("<h1 style='text-align: center; font-size: 32px;'>Dari kasus kekerasan yang terjadi di {}, berapa jumlah korban yang telah terlayani? bagaimana perbandingannya dengan jumlah korban terlapor?</h1>".format(string.capwords(kab_kota)), unsafe_allow_html=True)
st.write("\n")

col1, col2 = st.columns(2)
with col1:
    val4 = "jumlah"
    name4 = "korban"
    color4 = "korban"
    cmap4 = {"anak_perempuan": "#F77ED0", "anak_laki_laki": "#7ED0F7", "perempuan": "#D0F77E"}
    title4 = "Korban Terlapor di {} Tahun {}".format(string.capwords(kab_kota), tahun)

    if tahun == "2017-2021":
        if kab_kota == "jawa barat":
            data4 = df[df_name.index("total_korban_kabupaten_kota")].groupby("korban")["jumlah"].sum().reset_index()
            st.plotly_chart(pie_chart(data4, val4, name4, color4, cmap4, title4))

        else:
            data4 = df[df_name.index("total_korban_kabupaten_kota")].loc[df[df_name.index("total_korban_kabupaten_kota")]["kabupaten/kota"] == kab_kota]
            data4 = data4.groupby("korban")["jumlah"].sum().reset_index()
            st.plotly_chart(pie_chart(data4, val4, name4, color4, cmap4, title4))

    else:
        if kab_kota == "jawa barat":
            data4 = df[df_name.index("total_korban_kabupaten_kota")].groupby(["tahun", "korban"])["jumlah"].sum().reset_index()
            data4 = data4.loc[data4["tahun"] == tahun]
            st.plotly_chart(pie_chart(data4, val4, name4, color4, cmap4, title4))

        else:
            data4 = df[df_name.index("total_korban_kabupaten_kota")].loc[df[df_name.index("total_korban_kabupaten_kota")]["kabupaten/kota"] == kab_kota]
            data4 = data4.loc[data4["tahun"] == tahun]
            st.plotly_chart(pie_chart(data4, val4, name4, color4, cmap4, title4))

with col2:
    val5 = "jumlah_korban"
    name5 = "jenis_kelamin"
    color5 = "jenis_kelamin"
    cmap5 = {"perempuan": "#F77ED0", "laki-laki": "#7ED0F7"}
    title5 = "Korban Terlayani di {} Tahun {}".format(string.capwords(kab_kota), tahun)

    if tahun == 2017:
        st.write("Data tidak tersedia")

    elif tahun == "2017-2021":
        if kab_kota == "jawa barat":
            data5 = df[df_name.index("korban_terlayani")].groupby("jenis_kelamin")["jumlah_korban"].sum().reset_index()
            st.plotly_chart(pie_chart(data5, val5, name5, color5, cmap5, title5))  

        else:
            data5 = df[df_name.index("korban_terlayani")].loc[df[df_name.index("korban_terlayani")]["kabupaten/kota"] == kab_kota]
            data5 = data5.groupby("jenis_kelamin")["jumlah_korban"].sum().reset_index()
            st.plotly_chart(pie_chart(data5, val5, name5, color5, cmap5, title5))   

    else:
        if kab_kota == "jawa barat":
            data5 = df[df_name.index("korban_terlayani")].groupby(["tahun", "jenis_kelamin"])["jumlah_korban"].sum().reset_index()
            data5 = data5.loc[data5["tahun"] == tahun]
            st.plotly_chart(pie_chart(data5, val5, name5, color5, cmap5, title5))  
              
        else:
            data5 = df[df_name.index("korban_terlayani")].loc[df[df_name.index("korban_terlayani")]["kabupaten/kota"] == kab_kota]
            data5 = data5.loc[data5["tahun"] == tahun]
            st.plotly_chart(pie_chart(data5, val5, name5, color5, cmap5, title5))  

st.markdown("<p style='text-align: justify; font-size: 18px;'>Pada kedua grafik di atas, dapat dilihat bahwa jumlah korban yang terlayani masih sedikit jika dibandingkan dengan jumlah korban yang terdata/terlapor. Hal ini mungkin dapat disebabkan oleh beberapa hal, yaitu rasa malu dari korban untuk melapor, adanya tekanan dari pelaku kekerasan, dan korban yang tidak sadar bahwa dirinya menjadi korban kekerasan.</p>", unsafe_allow_html=True)
st.write("")
st.caption("Sumber data diperoleh dari https://opendata.jabarprov.go.id/")

st.caption("Portofolio lain dapat dilihat pada https://iqbalmyusuf.github.io/")
