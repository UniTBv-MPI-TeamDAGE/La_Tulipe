Feature: Shopping Cart

  As a customer
  I want to manage my shopping cart
  So that I can prepare my order

  # ---------------------------
  # ADD TO CART
  # ---------------------------

  Scenario: Add product to cart
    Given products exist in the catalog
    When the user adds the product to the cart
    Then the product is added to the cart
    And the cart count is increased

  Scenario: Add product with quantity
    Given products exist in the catalog
    When the user adds 5 units of a product to the cart
    Then the cart contains that product with quantity 5

  Scenario: Add same product multiple times
    Given the cart already contains a product with quantity 2
    When the user adds the same product again
    Then the product quantity becomes 3
    And the product is not duplicated as a separate item

  # ---------------------------
  # CART DISPLAY
  # ---------------------------

  Scenario: Display product with quantity and price
    Given the cart contains a product with quantity 5 and unit price 21
    When the cart is displayed
    Then the product is shown as "5 x 21"
    And the total price for that product is calculated correctly

  Scenario: Display total cart price
    Given the cart contains multiple products
    When the cart is displayed
    Then the total price of the cart is calculated correctly

  # ---------------------------
  # UPDATE QUANTITY
  # ---------------------------

  Scenario: Increase product quantity
    Given the cart contains a product with quantity 1
    When the user increases the quantity
    Then the product quantity becomes 2
    And the total price is updated correctly

  Scenario: Decrease product quantity
    Given the cart contains a product with quantity 2
    When the user decreases the quantity
    Then the product quantity becomes 1
    And the total price is updated correctly

  Scenario: Decrease quantity to zero removes product
    Given the cart contains a product with quantity 1
    When the user decreases the quantity
    Then the product is removed from the cart

  # ---------------------------
  # REMOVE FROM CART
  # ---------------------------

  Scenario: Remove product from cart
    Given the cart contains a product with quantity 5
    When the user removes the product
    Then the product is removed from the cart

  Scenario: Clear cart
    Given the cart contains multiple products
    When the user clears the cart
    Then the cart is empty

  # ---------------------------
  # PERSISTENCE
  # ---------------------------

  Scenario: Cart persists after page refresh
    Given the user has products in the cart
    When the page is refreshed
    Then the cart still contains the same products

  Scenario: Cart persists between pages
    Given the user has products in the cart
    When the user navigates between pages
    Then the cart still contains the same products

  Scenario: Cart persists after logout and login
    Given the user has products in the cart
    When the user logs out and logs back in
    Then the cart still contains the same products

  # ---------------------------
  # EDGE CASES
  # ---------------------------

  Scenario: Add product with zero quantity
    Given products exist in the catalog
    When the user tries to add a product with quantity 0
    Then the product is not added to the cart
    And an error message is displayed

  Scenario: Add product with negative quantity
    Given products exist in the catalog
    When the user tries to add a product with quantity -1
    Then the product is not added to the cart
    And an error message is displayed

  Scenario: Cannot add unavailable product
    Given a product is not available in the catalog
    When the user tries to add the product to the cart
    Then the product is not added to the cart
    And an error message is displayed

