Feature: Authentication

  As a user
  I want to register and login
  So that I can use the application

  Scenario: Inregistrare cu date valide
    Given utilizatorul este pe pagina de register
    When introduce un email valid si o parola valida
    And apasa butonul de inregistrare
    Then contul este creat
    And utilizatorul este redirectionat catre pagina de login

  Scenario: Inregistrare cu email duplicat
    Given exista deja un cont cu emailul "test@test.com"
    When utilizatorul incearca sa se inregistreze cu acelasi email
    Then primeste mesaj de eroare "Email deja utilizat"

  Scenario: Login succes → redirect home
    Given utilizatorul are cont valid
    When introduce email si parola corecte
    And apasa butonul de login
    Then autentificarea este reusita
    And utilizatorul este redirectionat catre pagina principala

  Scenario: Login parola gresita → eroare inline
    Given utilizatorul are cont valid
    When introduce email corect si parola gresita
    And apasa butonul de login
    Then autentificarea esueaza
    And se afiseaza mesaj de eroare "Parola incorecta"

  Scenario: Client acceseaza /admin → 403
    Given utilizatorul este autentificat ca "client"
    When acceseaza ruta "/admin"
    Then accesul este interzis
    And primeste raspuns 403