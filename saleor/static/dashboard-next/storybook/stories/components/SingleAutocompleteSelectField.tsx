import { storiesOf } from "@storybook/react";
import * as React from "react";

import Form from "../../../components/Form";
import SingleAutocompleteSelectField from "../../../components/SingleAutocompleteSelectField";
import Decorator from "../../Decorator";
import { ChoiceProvider } from "../../mock";

const suggestions = [
  "Afghanistan",
  "Åland Islands",
  "Albania",
  "Algeria",
  "American Samoa",
  "Andorra",
  "Angola",
  "Anguilla",
  "Antigua and Barbuda",
  "Argentina",
  "Armenia",
  "Aruba",
  "Australia",
  "Austria",
  "Azerbaijan",
  "Bangladesh",
  "Barbados",
  "Bahamas",
  "Bahrain",
  "Belarus",
  "Belgium",
  "Belize",
  "Benin",
  "Bermuda",
  "Bhutan",
  "Bolivia",
  "Bosnia and Herzegovina",
  "Botswana",
  "Brazil",
  "British Indian Ocean Territory",
  "British Virgin Islands",
  "Brunei Darussalam",
  "Bulgaria",
  "Burkina Faso",
  "Burma",
  "Burundi",
  "Cambodia",
  "Cameroon",
  "Canada",
  "Cape Verde",
  "Cayman Islands",
  "Central African Republic",
  "Chad",
  "Chile",
  "China",
  "Christmas Island",
  "Cocos (Keeling) Islands",
  "Colombia",
  "Comoros",
  "Congo-Brazzaville",
  "Congo-Kinshasa",
  "Cook Islands",
  "Costa Rica",
  "$_[",
  "Croatia",
  "Curaçao",
  "Cyprus",
  "Czech Republic",
  "Denmark",
  "Djibouti",
  "Dominica",
  "Dominican Republic",
  "East Timor",
  "Ecuador",
  "El Salvador",
  "Egypt",
  "Equatorial Guinea",
  "Eritrea",
  "Estonia",
  "Ethiopia",
  "Falkland Islands",
  "Faroe Islands",
  "Federated States of Micronesia",
  "Fiji",
  "Finland",
  "France",
  "French Guiana",
  "French Polynesia",
  "French Southern Lands",
  "Gabon",
  "Gambia",
  "Georgia",
  "Germany",
  "Ghana",
  "Gibraltar",
  "Greece",
  "Greenland",
  "Grenada",
  "Guadeloupe",
  "Guam",
  "Guatemala",
  "Guernsey",
  "Guinea",
  "Guinea-Bissau",
  "Guyana",
  "Haiti",
  "Heard and McDonald Islands",
  "Honduras",
  "Hong Kong",
  "Hungary",
  "Iceland",
  "India",
  "Indonesia",
  "Iraq",
  "Ireland",
  "Isle of Man",
  "Israel",
  "Italy",
  "Jamaica",
  "Japan",
  "Jersey",
  "Jordan",
  "Kazakhstan",
  "Kenya",
  "Kiribati",
  "Kuwait",
  "Kyrgyzstan",
  "Laos",
  "Latvia",
  "Lebanon",
  "Lesotho",
  "Liberia",
  "Libya",
  "Liechtenstein",
  "Lithuania",
  "Luxembourg",
  "Macau",
  "Macedonia",
  "Madagascar",
  "Malawi",
  "Malaysia",
  "Maldives",
  "Mali",
  "Malta",
  "Marshall Islands",
  "Martinique",
  "Mauritania",
  "Mauritius",
  "Mayotte",
  "Mexico",
  "Moldova",
  "Monaco",
  "Mongolia",
  "Montenegro",
  "Montserrat",
  "Morocco",
  "Mozambique",
  "Namibia",
  "Nauru",
  "Nepal",
  "Netherlands",
  "New Caledonia",
  "New Zealand",
  "Nicaragua",
  "Niger",
  "Nigeria",
  "Niue",
  "Norfolk Island",
  "Northern Mariana Islands",
  "Norway",
  "Oman",
  "Pakistan",
  "Palau",
  "Panama",
  "Papua New Guinea",
  "Paraguay",
  "Peru",
  "Philippines",
  "Pitcairn Islands",
  "Poland",
  "Portugal",
  "Puerto Rico",
  "Qatar",
  "Réunion",
  "Romania",
  "Russia",
  "Rwanda",
  "Saint Barthélemy",
  "Saint Helena",
  "Saint Kitts and Nevis",
  "Saint Lucia",
  "Saint Martin",
  "Saint Pierre and Miquelon",
  "Saint Vincent",
  "Samoa",
  "San Marino",
  "São Tomé and Príncipe",
  "Saudi Arabia",
  "Senegal",
  "Serbia",
  "Seychelles",
  "Sierra Leone",
  "Singapore",
  "Sint Maarten",
  "Slovakia",
  "Slovenia",
  "Solomon Islands",
  "Somalia",
  "South Africa",
  "South Georgia",
  "South Korea",
  "Spain",
  "Sri Lanka",
  "Sudan",
  "Suriname",
  "Svalbard and Jan Mayen",
  "Sweden",
  "Swaziland",
  "Switzerland",
  "Syria",
  "Taiwan",
  "Tajikistan",
  "Tanzania",
  "Thailand",
  "Togo",
  "Tokelau",
  "Tonga",
  "Trinidad and Tobago",
  "Tunisia",
  "Turkey",
  "Turkmenistan",
  "Turks and Caicos Islands",
  "Tuvalu",
  "Uganda",
  "Ukraine",
  "United Arab Emirates",
  "United Kingdom",
  "United States",
  "Uruguay",
  "Uzbekistan",
  "Vanuatu",
  "Vatican City",
  "Vietnam",
  "Venezuela",
  "Wallis and Futuna",
  "Western Sahara",
  "Yemen",
  "Zambia",
  "Zimbabwe"
].map(c => ({ label: c, value: c.toLocaleLowerCase().replace(/\s+/, "_") }));

storiesOf("Generics / SingleAutocompleteSelectField", module)
  .addDecorator(Decorator)
  .add("with loading data", () => (
    <Form initial={{ country: suggestions[0] }}>
      {({ change, data }) => (
        <ChoiceProvider choices={suggestions}>
          {({ choices, fetchChoices }) => (
            <SingleAutocompleteSelectField
              choices={choices}
              fetchChoices={fetchChoices}
              helperText={`Value: ${data.country.value}`}
              loading={true}
              name="country"
              onChange={change}
              placeholder="Select country"
              value={data.country}
            />
          )}
        </ChoiceProvider>
      )}
    </Form>
  ))
  .add("with loaded data", () => (
    <Form initial={{ country: suggestions[0] }}>
      {({ change, data }) => (
        <ChoiceProvider choices={suggestions}>
          {({ choices, fetchChoices }) => (
            <SingleAutocompleteSelectField
              choices={choices}
              fetchChoices={fetchChoices}
              helperText={`Value: ${data.country.value}`}
              loading={false}
              name="country"
              onChange={change}
              placeholder="Select country"
              value={data.country}
            />
          )}
        </ChoiceProvider>
      )}
    </Form>
  ))
  .add("with custom option", () => (
    <Form initial={{ country: suggestions[0] }}>
      {({ change, data }) => (
        <ChoiceProvider choices={suggestions}>
          {({ choices, fetchChoices, loading }) => (
            <SingleAutocompleteSelectField
              choices={choices}
              custom={true}
              fetchChoices={fetchChoices}
              helperText={`Value: ${data.country.value}`}
              loading={loading}
              name="country"
              onChange={change}
              placeholder="Select country"
              value={data.country}
            />
          )}
        </ChoiceProvider>
      )}
    </Form>
  ));
