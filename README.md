# MoneyRecogniser


## About

Money Recogniser is an API created using Django Rest Framework that allows to identifiy the currency and denomination of the banknote based on uploaded image.
It was created for student project as a part of Competention Project lecture on Łódź University of Technology.
The heart of the api, is model trained upon Microsoft Banknote-net model.
It can recognise over 120 banknotes (front and back sided) for following currencies:

- USD
- EUR
- INR
- PHPP
- AUD
- BRL
- CAD
- JPY
- MXN
- PKR
- SGD
- TRY
- NZD
- NNR
- MYR
- IDR
- PHP
- PLN (added esspecialy for this project)

## Installation

To run the project you need to have Docker installed on your machine.
Then you need to compose the project using following command:

```bash
docker-compose up
```

Then all required dependencies will be installed and the project will be ready to use.

## Usage

To use the API you need to send POST request to the following endpoint:

```
  /recognise/Bill
```
example request:
```json
{
    "image": "file"
}
```
where

the request should contain the image of the banknote in the body of the request.

The response will contain the currency and denomination of the banknote.

example response:
```json
{
    "currency": "USD",
    "denomination": 1,
    "confidence": 90.131013
}
```
If you will provide authentication token in the header of the request, you will be able to see the history of all requests made to the API by specific user.
To see the history you need to send GET request to the following endpoint:

```
  /money_scan
```
with the authentication token in the header of the request.

## Attributions

Microsoft BankNote-Net - Encryptor and Dataset for creating the project model

- Ttile: BankNote-Net: Open Dataset for Assistive Currency Recognition
- Authors; Felipe Oviedo, Srinivas Vinnakota, Eugene Seleznev, Hemant Malhotra, Saqib Shaikh & Juan Lavista Ferres
- Journal; https://arxiv.org/pdf/2204.03738.pdf
- Repository: https://github.com/microsoft/banknote-net
- Year: 2022

Django on Docker - for creating the project structure

- Thanks @mjhea0
- Repository: https://github.com/testdrivenio/django-on-docker/tree/main/app
