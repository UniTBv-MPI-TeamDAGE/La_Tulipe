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

  # ---------------------------
  # LOGIN
  # ---------------------------

  Scenario: Login cu date valide
    Given utilizatorul are un cont valid
    When introduce email si parola corecte
    And apasa butonul de login
    Then autentificarea este reusita
    And API raspunde cu status 200
    And primeste un JWT token
    And tokenul contine rolul utilizatorului

  Scenario: Login cu parola gresita
    Given utilizatorul are un cont valid
    When introduce email corect si parola gresita
    And apasa butonul de login
    Then API raspunde cu status 401
    And se afiseaza mesaj "Email sau parola incorecta"

  Scenario: Login cu email inexistent
    Given nu exista un cont cu emailul "nou@test.com"
    When utilizatorul incearca sa se logheze
    Then API raspunde cu status 401
    And se afiseaza mesaj "Email sau parola incorecta"

  Scenario: Token este salvat dupa login
    Given utilizatorul se logheaza cu succes
    When primeste JWT token
    Then tokenul este salvat in localStorage

  Scenario: Navbar se actualizeaza dupa login
    Given utilizatorul este logat
    When acceseaza pagina principala
    Then navbar afiseaza "Buna, [Nume]"

  Scenario: Logout sterge tokenul
    Given utilizatorul este logat
    When apasa butonul "Iesi din cont"
    Then tokenul este sters din localStorage
    And utilizatorul este redirectionat catre "/login"