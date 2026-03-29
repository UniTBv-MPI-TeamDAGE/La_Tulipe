Feature: Orders

  As a customer
  I want to place and view my orders
  So that I can receive my products

  # ---------------------------
  # CHECKOUT FLOW
  # ---------------------------

  Scenario: Cannot place order with empty cart
    Given the cart is empty
    When the user tries to place an order
    Then the order is not created
    And an error message is displayed

  Scenario: Start checkout from cart
    Given the user has products in the cart
    When the user clicks "Place order"
    Then the checkout page is displayed

  Scenario: Enter delivery address
    Given the user is on the checkout page
    When the user enters a valid delivery address
    Then the address is saved

  Scenario: Select payment method
    Given the user is on the checkout page
    When the user selects a payment method
    Then the payment method is saved

  # ---------------------------
  # ORDER CONFIRMATION
  # ---------------------------

  Scenario: Confirm order before placing
    Given the user has completed all required details
    When the user clicks "Place order"
    Then a confirmation dialog is displayed

  Scenario: Successful order placement
    Given the user confirms the order
    When the order is placed
    Then the order is created successfully
    And a confirmation message is displayed
    And the cart becomes empty

  # ---------------------------
  # ORDER DATA
  # ---------------------------

  Scenario: Order stores correct data
    Given the cart contains products with quantities and prices
    And a delivery cost is applied
    When the order is placed
    Then the order contains all products
    And each product has the correct quantity
    And the total price is saved correctly
    And the delivery cost is saved correctly

  Scenario: Free delivery applied
    Given the cart total price is greater than 150
    When the user places the order
    Then the delivery cost in the order is 0

  Scenario: Standard delivery applied
    Given the cart total price is less than 150
    When the user places the order
    Then the delivery cost is applied in the order

  # ---------------------------
  # MY ORDERS
  # ---------------------------

  Scenario: View my orders
    Given the user has placed orders
    When the user opens "My Orders"
    Then a list of orders is displayed

  Scenario: View order details
    Given the user has at least one order
    When the user selects an order
    Then the order details are displayed
    And the products are shown
    And the total price is shown
    And the delivery cost is shown

  # ---------------------------
  # EDGE CASES
  # ---------------------------

  Scenario: Cannot place order with unavailable product
    Given a product in the cart is no longer available
    When the user tries to place the order
    Then the order is not created
    And an error message is displayed