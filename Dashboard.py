from re import A, S
import pandas as pd
import streamlit as st
import plotly.express as px
import lorem
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
st.title("Eksplorasi Kasus Tindak Kekerasan di Jawa Barat Tahun 2017-2021")

st.write(lorem.paragraph())
st.write("\n")
st.write("\n")

# Memasukkan data ke dashboard
with st.sidebar:
    st.header("Filter data")
    tahun = st.selectbox("Pilih tahun", list_tahun)
    kab_kota = st.selectbox("Pilih kabupaten/kota", list_kab_kota)
    korban = st.selectbox("Pilih korban", ["anak laki-laki", "anak perempuan", "perempuan"])

# Membuat grafik yang berisi data kekerasan pertahun/per-kabupaten/kota
col1, col2 = st.columns(2)
with col2:
    tipe = st.selectbox("Pilih jenis visualisasi", ["Data per tahun", "Data per kabupaten/kota"])
    if tipe == "Data per tahun":
        if tahun == "2017-2021":
            data1 = df[df_name.index("total_korban_kabupaten_kota")].groupby(["kabupaten/kota", "korban"]).sum().reset_index()
            fig = px.bar(data1, x='jumlah', y='kabupaten/kota', color='korban', 
                         color_discrete_map={'anak_laki_laki': '#7ED0F7', 'anak_perempuan': '#D0F77E', 'perempuan' : '#F77ED0'},
                         width=700, height=600)
            fig.update_layout(title={ 'text': "Data tahun {}".format(tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            fig.update_yaxes(categoryorder='total descending')
            st.plotly_chart(fig)

        else:
            data1 = df[df_name.index("total_korban_kabupaten_kota")].loc[df[df_name.index("total_korban_kabupaten_kota")]["tahun"] == tahun]
            fig = px.bar(data1, x='jumlah', y='kabupaten/kota', color='korban', 
                         color_discrete_map={'anak_laki_laki': '#7ED0F7', 'anak_perempuan': '#D0F77E', 'perempuan' : '#F77ED0'},
                         width=700, height=600)
            fig.update_layout(title={ 'text': "Data tahun {}".format(tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            fig.update_yaxes(categoryorder='total descending')
            st.plotly_chart(fig)
    else:
        if kab_kota == "jawa barat":
            data1 = df[df_name.index("total_korban_kabupaten_kota")].groupby(["tahun", "korban"]).sum().reset_index()
            data1["tahun"] = data1["tahun"].astype(str)
            fig = px.line(data1, x='tahun', y='jumlah', color='korban', 
                         color_discrete_map={'anak_laki_laki': '#7ED0F7', 'anak_perempuan': '#D0F77E', 'perempuan' : '#F77ED0'},
                         width=700, height=600)
            fig.update_layout(title={ 'text': "Data untuk {}".format(kab_kota),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            st.plotly_chart(fig)
        else:
            data1 = df[df_name.index("total_korban_kabupaten_kota")].loc[df[df_name.index("total_korban_kabupaten_kota")]["kabupaten/kota"] == kab_kota]
            data1["tahun"] = data1["tahun"].astype(str)
            fig = px.line(data1, x='tahun', y='jumlah', color='korban', 
                         color_discrete_map={'anak_laki_laki': '#7ED0F7', 'anak_perempuan': '#D0F77E', 'perempuan' : '#F77ED0'},
                         width=700, height=600)
            fig.update_layout(title={ 'text': "Data untuk {}".format(kab_kota),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            st.plotly_chart(fig)

with col1:
    if tipe == "Data per tahun":
        st.subheader("Data kekerasan pada tahun {}".format(tahun))
        st.write(lorem.paragraph())
    else:
        st.subheader("Data kekerasan di {}".format(kab_kota))
        st.write(lorem.paragraph())      

# Membuat section untuk grafik baru
st.write("\n")
st.write("\n")
col1, col2 = st.columns(2)

# Membuat grafik yang berisi jenis kekerasan yang dialami oleh korban
with col1:
    st.subheader("Jenis kekerasan yang dialami oleh korban {} di {}".format(korban, kab_kota))
    if kab_kota == "jawa barat":
        if korban == "anak laki-laki":
            data2 = df[df_name.index("jumlah_korban")].groupby(["tahun", "jenis_kekerasan"])["jumlah_korban_anak_laki-laki"].sum().reset_index()
            fig = px.bar(data2, x='tahun', y='jumlah_korban_anak_laki-laki', color='jenis_kekerasan', 
                         color_discrete_map={"eksploitasi": "#ADADAD", "fisik": "#7ED0F7", "lainnya": "#7E94F7", "penelantaran": "#F77ED0", "psikis": "#F77E94", "seksual": "#D0F77E", "trafficking": "#94F77E"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Jenis kekerasan",
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            fig.update_yaxes(title="jumlah korban")
            st.plotly_chart(fig)

        elif korban == "anak perempuan":
            data2 = df[df_name.index("jumlah_korban")].groupby(["tahun", "jenis_kekerasan"])["jumlah_korban_anak_perempuan"].sum().reset_index()
            fig = px.bar(data2, x='tahun', y='jumlah_korban_anak_perempuan', color='jenis_kekerasan', 
                         color_discrete_map={"eksploitasi": "#ADADAD", "fisik": "#7ED0F7", "lainnya": "#7E94F7", "penelantaran": "#F77ED0", "psikis": "#F77E94", "seksual": "#D0F77E", "trafficking": "#94F77E" },
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Jenis kekerasan",
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            fig.update_yaxes(title="jumlah korban")
            st.plotly_chart(fig)

        else:
            data2 = df[df_name.index("jumlah_korban")].groupby(["tahun", "jenis_kekerasan"])["jumlah_korban_perempuan"].sum().reset_index()
            fig = px.bar(data2, x='tahun', y='jumlah_korban_perempuan', color='jenis_kekerasan', 
                         color_discrete_map={"eksploitasi": "#ADADAD", "fisik": "#7ED0F7", "lainnya": "#7E94F7", "penelantaran": "#F77ED0", "psikis": "#F77E94", "seksual": "#D0F77E", "trafficking": "#94F77E" },
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Jenis kekerasan",
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            fig.update_yaxes(title="jumlah korban")
            st.plotly_chart(fig)

    else:
        if korban == "anak laki-laki":
            data2 = df[df_name.index("jumlah_korban")].loc[df[df_name.index("jumlah_korban")]["kabupaten/kota"] == kab_kota]
            fig = px.bar(data2, x='tahun', y='jumlah_korban_anak_laki-laki', color='jenis_kekerasan', 
                         color_discrete_map={"eksploitasi": "#ADADAD", "fisik": "#7ED0F7", "lainnya": "#7E94F7", "penelantaran": "#F77ED0", "psikis": "#F77E94", "seksual": "#D0F77E", "trafficking": "#94F77E"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Jenis kekerasan",
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            fig.update_yaxes(title="jumlah korban")
            st.plotly_chart(fig)

        elif korban == "anak perempuan":
            data2 = df[df_name.index("jumlah_korban")].loc[df[df_name.index("jumlah_korban")]["kabupaten/kota"] == kab_kota]
            fig = px.bar(data2, x='tahun', y='jumlah_korban_anak_perempuan', color='jenis_kekerasan', 
                         color_discrete_map={"eksploitasi": "#ADADAD", "fisik": "#7ED0F7", "lainnya": "#7E94F7", "penelantaran": "#F77ED0", "psikis": "#F77E94", "seksual": "#D0F77E", "trafficking": "#94F77E" },
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Jenis kekerasan",
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            fig.update_yaxes(title="jumlah korban")
            st.plotly_chart(fig)

        else:
            data2 = df[df_name.index("jumlah_korban")].loc[df[df_name.index("jumlah_korban")]["kabupaten/kota"] == kab_kota]
            fig = px.bar(data2, x='tahun', y='jumlah_korban_perempuan', color='jenis_kekerasan', 
                         color_discrete_map={"eksploitasi": "#ADADAD", "fisik": "#7ED0F7", "lainnya": "#7E94F7", "penelantaran": "#F77ED0", "psikis": "#F77E94", "seksual": "#D0F77E", "trafficking": "#94F77E" },
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Jenis kekerasan",
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
            fig.update_yaxes(title="jumlah korban")
            st.plotly_chart(fig)
    st.write(lorem.paragraph())

# Grafik tempat terjadinya tindak kekerasan
with col2:
    st.subheader("Distribusi tempat terjadinya tindak kekerasan di {} berdasarkan tahun kejadian".format(kab_kota))
    if kab_kota == "jawa barat":
        data3 = df[df_name.index("tempat_kejadian")].groupby(["tahun", "tempat_kejadian"])["jumlah_kekerasan"].sum().reset_index()
        fig = px.bar(data3, x='tahun', y='jumlah_kekerasan', color='tempat_kejadian', 
                     color_discrete_map={"rumah tangga": "#D77EF7", "tempat kerja": "#7EF79A", "lainnya": "#F79A7E", "sekolah": "#F7D77E", "fasilitas umum": "#7EF7D7", "lembaga pendidikan kilat": "#9A7EF7"},
                     width=600, height=600)
        fig.update_layout(title={ 'text': "Tempat kejadian kekerasan",
                                  'y':0.97,
                                  'x':0.5,
                                  'xanchor': 'center',
                                  'yanchor': 'top'},
                          title_font_size=24)
        fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
        fig.update_yaxes(title="jumlah korban")
        st.plotly_chart(fig)

    else:
        data3 = df[df_name.index("tempat_kejadian")].loc[df[df_name.index("tempat_kejadian")]["kabupaten/kota"] == kab_kota]
        fig = px.bar(data3, x='tahun', y='jumlah_kekerasan', color='tempat_kejadian', 
                     color_discrete_map={"rumah tangga": "#D77EF7", "tempat kerja": "#7EF79A", "lainnya": "#F79A7E", "sekolah": "#F7D77E", "fasilitas umum": "#7EF7D7", "lembaga pendidikan kilat": "#9A7EF7"},
                     width=600, height=600)
        fig.update_layout(title={ 'text': "Tempat kejadian kekerasan",
                                  'y':0.97,
                                  'x':0.5,
                                  'xanchor': 'center',
                                  'yanchor': 'top'},
                          title_font_size=24)
        fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})
        fig.update_yaxes(title="jumlah korban")
        st.plotly_chart(fig)
    st.write(lorem.paragraph())

# Membuat section yang membandingkan antara kasus yang terlapor dan kasus yang terlayani
st.write("\n")
st.write("\n")
st.subheader("Perbandingan antara kasus terlapor dengan kasus yang terlayani")
st.write(lorem.paragraph())

col1, col2 = st.columns(2)
with col1:
    if tahun == "2017-2021":
        if kab_kota == "jawa barat":
            data4 = df[df_name.index("total_korban_kabupaten_kota")].groupby("korban")["jumlah"].sum().reset_index()
            fig = px.pie(data4, values='jumlah', names='korban', color="korban",
                         color_discrete_map={"anak_perempuan": "#F77ED0", "anak_laki_laki": "#7ED0F7", "perempuan": "#D0F77E"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Korban terlapor di {} tahun {}".format(kab_kota, tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            st.plotly_chart(fig)
        else:
            data4 = df[df_name.index("total_korban_kabupaten_kota")].loc[df[df_name.index("total_korban_kabupaten_kota")]["kabupaten/kota"] == kab_kota]
            data4 = data4.groupby("korban")["jumlah"].sum().reset_index()
            fig = px.pie(data4, values='jumlah', names='korban', color="korban",
                         color_discrete_map={"anak_perempuan": "#F77ED0", "anak_laki_laki": "#7ED0F7", "perempuan": "#D0F77E"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Korban terlapor di {} tahun {}".format(kab_kota, tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            st.plotly_chart(fig)  
    else:
        if kab_kota == "jawa barat":
            data4 = df[df_name.index("total_korban_kabupaten_kota")].groupby(["tahun", "korban"])["jumlah"].sum().reset_index()
            data4 = data4.loc[data4["tahun"] == tahun]
            fig = px.pie(data4, values='jumlah', names='korban', color="korban",
                         color_discrete_map={"anak_perempuan": "#F77ED0", "anak_laki_laki": "#7ED0F7", "perempuan": "#D0F77E"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Korban terlapor di {} tahun {}".format(kab_kota, tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            st.plotly_chart(fig)
        else:
            data4 = df[df_name.index("total_korban_kabupaten_kota")].loc[df[df_name.index("total_korban_kabupaten_kota")]["kabupaten/kota"] == kab_kota]
            data4 = data4.loc[data4["tahun"] == tahun]
            fig = px.pie(data4, values='jumlah', names='korban', color="korban",
                         color_discrete_map={"anak_perempuan": "#F77ED0", "anak_laki_laki": "#7ED0F7", "perempuan": "#D0F77E"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Korban terlapor di {} tahun {}".format(kab_kota, tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            st.plotly_chart(fig)

with col2:
    if tahun == 2017:
        st.write("Data tidak tersedia")

    elif tahun == "2017-2021":
        if kab_kota == "jawa barat":
            data5 = df[df_name.index("korban_terlayani")].groupby("jenis_kelamin")["jumlah_korban"].sum().reset_index()
            fig = px.pie(data5, values='jumlah_korban', names='jenis_kelamin', color="jenis_kelamin",
                         color_discrete_map={"perempuan": "#F77ED0", "laki-laki": "#7ED0F7"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Korban terlayani di {} tahun {}".format(kab_kota, tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            st.plotly_chart(fig)
        else:
            data5 = df[df_name.index("korban_terlayani")].loc[df[df_name.index("korban_terlayani")]["kabupaten/kota"] == kab_kota]
            data5 = data5.groupby("jenis_kelamin")["jumlah_korban"].sum().reset_index()
            fig = px.pie(data5, values='jumlah_korban', names='jenis_kelamin', color="jenis_kelamin",
                         color_discrete_map={"perempuan": "#F77ED0", "laki-laki": "#7ED0F7"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Korban terlayani di {} tahun {}".format(kab_kota, tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            st.plotly_chart(fig)        

    else:
        if kab_kota == "jawa barat":
            data5 = df[df_name.index("korban_terlayani")].groupby(["tahun", "jenis_kelamin"])["jumlah_korban"].sum().reset_index()
            data5 = data5.loc[data5["tahun"] == tahun]
            fig = px.pie(data5, values='jumlah_korban', names='jenis_kelamin', color="jenis_kelamin",
                         color_discrete_map={"perempuan": "#F77ED0", "laki-laki": "#7ED0F7"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Korban terlayani di {} tahun {}".format(kab_kota, tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            st.plotly_chart(fig)
        else:
            data5 = df[df_name.index("korban_terlayani")].loc[df[df_name.index("korban_terlayani")]["kabupaten/kota"] == kab_kota]
            data5 = data5.loc[data5["tahun"] == tahun]
            fig = px.pie(data5, values='jumlah_korban', names='jenis_kelamin', color="jenis_kelamin",
                         color_discrete_map={"perempuan": "#F77ED0", "laki-laki": "#7ED0F7"},
                         width=600, height=600)
            fig.update_layout(title={ 'text': "Korban terlayani di {} tahun {}".format(kab_kota, tahun),
                                      'y':0.97,
                                      'x':0.5,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_size=24)
            st.plotly_chart(fig)

st.write(lorem.paragraph())
st.write("")
st.caption("Sumber data diperoleh dari https://opendata.jabarprov.go.id/")
