import streamlit as st
import pickle
from datetime import datetime

import pathlib
from pathlib import Path

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

filename = "model.sv"
model = pickle.load(open(filename,'rb'))

symptoms_d = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}
comorbidities_d = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
medicines_d = {0: 1, 1: 2, 2: 3, 3: 4}

title = "App Health"

def main():

	st.set_page_config(page_title=title)
	overview = st.container()
	left, right = st.columns(2)
	prediction = st.container()

	st.image("https://www.medistore.com.pl/_ipx/f_jpeg,s_1536x614/https://prod-api.medistore.com.pl/media/amasty/blog/cache/s/e/1000/400/serce.jpg")

	with overview:
		st.title(title)

	with left:
	    symptomps_radio = st.radio("Objawy", list(symptoms_d.keys()), format_func=lambda x : symptoms_d[x])
	    comorbidities_radio = st.radio("Choroby współistniejące", list(comorbidities_d.keys()), format_func=lambda x : comorbidities_d[x])
	    medicines_radio = st.radio("Leki", list(medicines_d.keys()), format_func=lambda x : medicines_d[x])
	    
	with right:
		age_slider = st.slider("Wiek", value=1, min_value=11, max_value=77)
		height_slider = st.slider("Wzrost", min_value=160, max_value=200)

	data = [[symptomps_radio, age_slider, comorbidities_radio, height_slider, medicines_radio]]
	survival = model.predict(data)
	s_confidence = model.predict_proba(data)

	with prediction:
		st.subheader("Czy taka osoba zachoruje na serce?")
		st.subheader(("Tak" if survival[0] == 1 else "Nie"))
		st.write("Pewność predykcji {0:.2f} %".format(s_confidence[0][survival][0] * 100))

if __name__ == "__main__":
    main()