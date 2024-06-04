import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Załadowanie danych
users = pd.read_csv('users.csv')
boats = pd.read_csv('boats.csv')
bookings = pd.read_csv('bookings.csv')

# zapis rezerwacji
def save_booking(userId, boatId, dateFrom, days):
    new_booking = pd.DataFrame({
        'userId': [userId],
        'boatId': [boatId],
        'dateFrom': [dateFrom],
        'days': [days]
    })
    new_booking.to_csv('bookings.csv', mode='a', header=False, index=False)

# Strona główna
st.title('Wypożyczalnia Motorówek')
st.write('Witamy w naszej wypożyczalni motorówek!')

# Panel sprawdzania dostępnych przedmiotów do wypożyczenia
st.header('Dostępne motorówki')
st.table(boats)

# Panel wypożyczenia
st.header('Wypożycz motorówkę')
user_id = st.selectbox('Wybierz użytkownika', users['id'].tolist())
boat_id = st.selectbox('Wybierz motorówkę', boats['id'].tolist())
date_from = st.date_input('Data rozpoczęcia', datetime.date.today())
days = st.number_input('Ilość dni', min_value=1, step=1)

if st.button('Dodaj rezerwację'):
    save_booking(user_id, boat_id, date_from, days)
    st.success('Rezerwacja została dodana!')

# Panel sprawdzania wypożyczeń po identyfikatorze klienta
st.header('Sprawdź swoje wypożyczenia')
check_user_id = st.selectbox('Wybierz użytkownika do sprawdzenia', users['id'].tolist())
user_bookings = bookings[bookings['userId'] == check_user_id]
user_bookings = user_bookings.merge(boats, left_on='boatId', right_on='id')
st.table(user_bookings[['brand', 'model', 'dateFrom', 'days']])

# Wykres ilości wypożyczeń w obecnym miesiącu
st.header('Ilość wypożyczeń w obecnym miesiącu')
bookings['dateFrom'] = pd.to_datetime(bookings['dateFrom'])
bookings['month'] = bookings['dateFrom'].dt.month
bookings['day'] = bookings['dateFrom'].dt.day
current_month = datetime.date.today().month
month_bookings = bookings[bookings['month'] == current_month]
daily_bookings = month_bookings['day'].value_counts().sort_index()

fig, ax = plt.subplots()
ax.plot(daily_bookings.index, daily_bookings.values)
ax.set_xlabel('Dzień miesiąca')
ax.set_ylabel('Ilość wypożyczeń')
ax.set_title('Ilość wypożyczeń w bieżącym miesiącu')

st.pyplot(fig)
