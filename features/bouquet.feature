Feature: Bouquet Builder

  As a customer
  I want to create a custom bouquet
  So that I can personalize my order

  # ---------------------------
  # BUILD BOUQUET
  # ---------------------------

  Scenario: View available flowers
    Given flowers exist in the catalog
    When the user opens the bouquet builder page
    Then a list of available flowers is displayed

  Scenario: Add flowers to bouquet
    Given the user is on the bouquet builder page
    When the user adds 3 roses to the bouquet
    Then the bouquet contains 3 roses

  Scenario: Add multiple types of flowers
    Given the user is on the bouquet builder page
    When the user adds 2 tulips and 3 roses
    Then the bouquet contains all selected flowers

  Scenario: Remove flowers from bouquet
    Given the bouquet contains flowers
    When the user removes a flower
    Then the bouquet is updated

  # ---------------------------
  # PRICE CALCULATION
  # ---------------------------

  Scenario: Calculate bouquet price
    Given the bouquet contains flowers with known prices
    When the bouquet is updated
    Then the total price is calculated correctly

  Scenario: Apply discount for large bouquet
    Given the bouquet contains at least 5 flowers
    When the bouquet price is calculated
    Then a discount is applied

  Scenario: Update flower quantity in bouquet
    Given the bouquet contains flowers
    When the user increases or decreases the quantity
    Then the bouquet is updated
    And the total price is updated correctly

  # ---------------------------
  # ADD TO CART
  # ---------------------------

  Scenario: Add bouquet to cart
    Given the bouquet is ready
    When the user adds the bouquet to the cart
    Then the bouquet is added as a single item in the cart

  Scenario: Bouquet appears in cart with correct price
    Given the bouquet is added to the cart
    When the cart is displayed
    Then the bouquet price is correct

  # ---------------------------
  # EDGE CASES
  # ---------------------------

  Scenario: Cannot create empty bouquet
    Given the bouquet is empty
    When the user tries to add it to the cart
    Then the bouquet is not added
    And an error message is displayed

  Scenario: Clear bouquet
    Given the bouquet contains flowers
    When the user clears the bouquet
    Then the bouquet becomes empty