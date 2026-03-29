Feature: Product Catalog

  As a customer
  I want to browse and search products
  So that I can find flowers to buy

  # ---------------------------
  # BROWSING
  # ---------------------------

  Scenario: View product list
    Given the user is on the Home page
    When the page loads
    Then a list of products is displayed
    And each product shows name, price, category, description and image

  Scenario: Empty catalog
    Given there are no products in the database
    When the user opens the Home page
    Then a message "No products available" is displayed

  # ---------------------------
  # SEARCH
  # ---------------------------

  Scenario: Search products by name
    Given products exist in the catalog
    When the user searches for "rose"
    Then only products with name containing "rose" are displayed

  Scenario: Search is case insensitive
    Given products exist in the catalog
    When the user searches for "ROSE"
    Then only products with name containing "rose" are displayed

  Scenario: Search matches partial words
    Given products exist in the catalog
    When the user searches for "ros"
    Then only products with name containing "rose" are displayed

  Scenario: Search returns no results
    Given products exist in the catalog
    When the user searches for "xyz"
    Then no products are displayed
    And message "No results found" is shown

  Scenario: Empty search shows all products
    Given products exist in the catalog
    When the user clears the search input
    Then all products are displayed

  # ---------------------------
  # FILTERING
  # ---------------------------

  Scenario: Filter products by category
    Given products exist in multiple categories
    When the user selects category "tulips"
    Then only products from "tulips" category are shown

  Scenario: Filter products by price range
    Given products exist with different prices
    When the user selects price range 50-100
    Then only products within that range are displayed

  Scenario: Filter products by category and price
    Given products exist in multiple categories and prices
    When the user selects category "tulips"
    And selects price range 50-100
    Then only products matching both filters are displayed

  Scenario: Reset filters
    Given filters are applied
    When the user clears all filters
    Then all products are displayed

  Scenario: Sort products by price ascending
    Given products exist with different prices
    When the user selects "Sort by price ascending"
    Then products are displayed from lowest to highest price

  Scenario: Sort products by price descending
    Given products exist with different prices
    When the user selects "Sort by price descending"
    Then products are displayed from highest to lowest price

  Scenario: Filter returns no products
    Given products exist in the catalog
    When the user selects a category with no products
    Then no products are displayed
    And message "No products found" is shown