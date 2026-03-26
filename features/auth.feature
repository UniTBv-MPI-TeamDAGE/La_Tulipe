Feature: Authentication

  As a user
  I want to register and login
  So that I can use the application

  # ---------------------------
  # REGISTER
  # ---------------------------

  Scenario: Inregistrare cu date valide
    Given utilizatorul este pe pagina de register
    When introduce nume valid, email valid si parola valida
    And parola are minim 8 caractere
    And apasa butonul de inregistrare
    Then contul este creat
    And API raspunde cu status 201
    And utilizatorul este redirectionat catre pagina principala

  Scenario: Inregistrare cu email duplicat
    Given exista deja un cont cu emailul "test@test.com"
    When utilizatorul incearca sa se inregistreze cu acelasi email
    Then API raspunde cu status 409
    And se afiseaza mesaj "Email-ul este deja folosit"

  Scenario: Parola prea scurta
    Given utilizatorul este pe pagina de register
    When introduce o parola cu mai putin de 8 caractere
    Then API raspunde cu status 400
    And se afiseaza mesaj de eroare pentru parola

  Scenario: Parolele nu se potrivesc
    Given utilizatorul este pe pagina de register
    When introduce parola si confirmare diferite
    Then se afiseaza mesaj "Parolele nu se potrivesc"

  Scenario: Parola este criptata in baza de date
    Given utilizatorul se inregistreaza cu succes
    When datele sunt salvate in baza de date
    Then parola nu este stocata in plain text
    And este stocata criptat folosind bcrypt