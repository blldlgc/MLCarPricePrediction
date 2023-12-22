import streamlit as st
import pandas as pd
import  joblib



def main():



    st.title('2. El Araç Fiyat Tahmin Uygulamasına Hoşgeldiniz 🚗')

    st.markdown(
            """
            Bu projede otokocikinciel.com sitesi üzerinden 1080 adet araba verisi çekilmiş
            ve incelendikten sonra algoritmalar için en uyumlu hale gelecek şekilde düzenleniştir.
             Bu veriler kullanılarak makine öğrenmesi modelleri eğitilmiş ve içlerinden en iyi sonuç 
             veren model seçilerek fiyat tahmin uygulaması oluşturulmuştur. Projede kullanılan araç verileri
             2023 Aralık ayına aittir.

            """)

    predict()

def predict():
    markalar = pd.read_csv('data/markalar.csv')

    st.title('2. El Araç Fiyat Tahmin Uygulaması ')

    selected_brand = marka_index(markalar,st.selectbox('Aracınızın Markasını Seçiniz..',markalar))

    selected_km = st.number_input('Kilometre:', min_value=6000, max_value=500000)
    st.write("Kilometre: " + str(selected_km))
    selected_km = selected_km/1000


    selected_year = st.number_input('Model Yılı:', min_value=2000, max_value=2023)
    st.write("Model Yılı: "+str(selected_year))

    selected_engine = st.slider('Motor Hacmi: ', min_value=1.0, max_value=2.5, step=0.1)
    st.write("Motor Hacmi: "+str(selected_engine)+" Litre")
    selected_engine = selected_engine * 10


    gear_options = ("Manuel", "Otomatik", "Yarı Otomatik")
    selected_gear = st.selectbox("Vites Tipi:", range(len(gear_options)), format_func=lambda x: gear_options[x])

    st.write("option:", gear_options[selected_gear])
    st.write("index:", selected_gear) #TODO silincek

    fuel_options = ("Dizel", "Benzin", "Hibrit", "LPG", "Elektrik")
    selected_fuel = st.selectbox("Yakıt Türü:", range(len(fuel_options)), format_func=lambda x: fuel_options[x])

    st.write("option:", fuel_options[selected_fuel])
    st.write("index:", selected_fuel) #TODO silinecek

    #drive_options = ("Arkadan", "Önden")
    #selected_drive = st.selectbox("Çekiş Tipi:", range(len(drive_options)), format_func=lambda x: drive_options[x])

    #st.write("option:", drive_options[selected_drive])
    #st.write("index:", selected_drive)  # TODO silinecek

    prediction_value = create_prediction_value(selected_km,selected_brand,selected_year,selected_engine,selected_gear,selected_fuel)


    if st.button("Tahmin Yap"):
        result = predict_models(prediction_value)
        if result != None:
            st.success("Tahmin Başarılı")
            st.subheader("Tahmin Edilen Fiyat: "+ result + "TL")
        else:
            st.error('Tahmin yaparken hata meydana geldi!')





def marka_index(markalar,marka):
    index = int(markalar[markalar["Markalar"]==marka].index.values)
    return index


def create_prediction_value(kilometre, marka, model_yili, motor_hacmi, vites_tipi, yakit_turu,):
    res = pd.DataFrame(data=
                       {'Kilometre': [kilometre], 'Marka': [marka], 'Model_Yili': [model_yili],
                        'Motor_Hacmi': [motor_hacmi], 'Vites_Tipi': [vites_tipi],
                        'Yakit_Turu': [yakit_turu]})
    return res

def predict_models(res):
    rf_model = joblib.load('data/rf_model.sav')
    result = str(int(rf_model.predict(res))).strip('[]')
    return result

if __name__ == "__main__":
    main()
