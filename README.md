AI-Powered Real Estate Agent
============================
This application predicts the property value (or potential "sale value") for a house in the Ames, Iowa region based on a number of features that I selected as most important:
* Bedroom: Number of bedrooms above basement level
* CentralAir: Central air conditioning
* GarageCond: Garage condition (null if there is no garage)
* LotArea: Lot size in square feet
* MSSubClass: The building class
* Neighborhood: Physical locations within Ames city limits
* OverallQual: Overall material and finish quality
* TotRmsAbvGrd: Total rooms above ground (does not include bathrooms)
* YearBuilt: Original construction date
* YearRemodAdd: Remodel date

The user will describe a model to the application and address all of these features. Note that we use `GarageCond` during training as a marker of whether or not the house has a garage; it was mapped to a new feature, `HasGarage`. When providing information about the house, the user simply mentions whether or not the house has a garage.

As for lot area, this is a numeric feature, but for ease of use, the user will be asked to describe if the house is on a small, medium or large lot, as per these definitions:
* small lot < 5000 sqft
* 5000 <= medium < 12000 sqft
* large >= 12000 sqft

There are other features that will be hard for the user to describe. We'll explain how they're handled shortly.
* MSSubClass
* OverallQual
* YearBuilt
* YearRemodAdd
