import streamlit as st
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

sleep_time = 2

def get_driver():

    driver = webdriver.Chrome()
    driver.get("https://misiir.sii.cl/cgi_misii/siihome.cgi")

    return driver

def login(driver):

    sbox = driver.find_element(by=By.NAME, value='rutcntr')
    sbox.send_keys(st.secrets.sii_credentials.username)
    sleep(sleep_time)

    sbox = driver.find_element(by=By.NAME, value='clave')
    sbox.send_keys(st.secrets.sii_credentials.password)
    sleep(sleep_time)

    submit_button = driver.find_element(by=By.ID, value="bt_ingresar")
    submit_button.click()

def fill_table(driver, RUT, articulos):

    sbox = driver.find_element(by=By.NAME, value='EFXP_RUT_RECEP')
    sbox.send_keys(RUT.split('-')[0].replace('.', ''))
    sleep(sleep_time)

    sbox = driver.find_element(by=By.NAME, value='EFXP_DV_RECEP')
    sbox.send_keys(RUT.split('-')[1])
    sleep(sleep_time)

    sbox = driver.find_element(by=By.NAME, value='AGREGA_DETALLE')
    sbox.click()
    sleep(sleep_time)

    for i, articulo in enumerate(articulos):

        sbox = driver.find_element(by=By.NAME, value=f'EFXP_NMB_0{i+1}')
        sbox.send_keys(articulo[3])
        sleep(sleep_time)

        sbox = driver.find_element(by=By.NAME, value=f'EFXP_QTY_0{i+1}')
        sbox.send_keys(str(articulo[2]))
        sleep(sleep_time)

        sbox = driver.find_element(by=By.NAME, value=f'EFXP_PRC_0{i+1}')
        sbox.send_keys(str(articulo[4]))
        sleep(sleep_time)

        sbox = driver.find_element(by=By.NAME, value='AGREGA_DETALLE')
        sbox.click()
        sleep(sleep_time)

def main(RUT, articulos):
    driver = get_driver()
    login(driver)
    sleep(sleep_time)
    driver.get("https://www1.sii.cl/cgi-bin/Portal001/mipeLaunchPage.cgi?OPCION=33&amp;TIPO=4")
    fill_table(driver, RUT, articulos)
    validate = driver.find_element(by=By.NAME, value='Button_Update')
    validate.click()
    sleep(sleep_time)
    sign = driver.find_element(by=By.NAME, value='btnSign')
    sign.click()

    driver.close()
    