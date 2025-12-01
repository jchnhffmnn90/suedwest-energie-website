# Tarifrechner Embed - Implementation Guide

## Overview

The Tarifrechner (Tariff Calculator) embed feature allows you to integrate an external calculator widget into your website.

## Configuration

Add the following to your `.env` file:

```env
# Tarifrechner Configuration
TARIFRECHNER_ENABLED=True
TARIFRECHNER_TYPE=iframe  # or "script"
TARIFRECHNER_URL=https://example.com/calculator
TARIFRECHNER_SCRIPT=<script src="..."></script>
TARIFRECHNER_HEIGHT=600px
```

## Configuration Options

### TARIFRECHNER_ENABLED
- **Type**: Boolean
- **Default**: `True`
- **Description**: Enable or disable the Tarifrechner section entirely

### TARIFRECHNER_TYPE
- **Type**: String
- **Options**: `"iframe"` or `"script"`
- **Default**: `"iframe"`
- **Description**: Type of embed to use

### TARIFRECHNER_URL
- **Type**: String
- **Description**: URL for iframe embed (when TARIFRECHNER_TYPE=iframe)
- **Example**: `https://calculator.example.com/embed`

### TARIFRECHNER_SCRIPT
- **Type**: String
- **Description**: HTML/JavaScript code for script embed (when TARIFRECHNER_TYPE=script)
- **Example**: `<script src="https://example.com/calculator.js"></script><div id="calculator"></div>`

### TARIFRECHNER_HEIGHT
- **Type**: String
- **Default**: `"600px"`
- **Description**: Height of the embedded calculator

## Usage Examples

### Example 1: iFrame Embed

```env
TARIFRECHNER_ENABLED=True
TARIFRECHNER_TYPE=iframe
TARIFRECHNER_URL=https://www.tarifcheck.de/stromrechner/embed
TARIFRECHNER_HEIGHT=800px
```

### Example 2: Script Embed

```env
TARIFRECHNER_ENABLED=True
TARIFRECHNER_TYPE=script
TARIFRECHNER_SCRIPT=<script src="https://www.verivox.de/widget.js"></script><div class="verivox-calculator"></div>
TARIFRECHNER_HEIGHT=700px
```

### Example 3: Disable Tarifrechner

```env
TARIFRECHNER_ENABLED=False
```

## Page Position

The Tarifrechner appears on the homepage in the following order:
1. Hero
2. Service Models
3. Benefits
4. About
5. Services
6. **→ Tarifrechner** ← (positioned here)
7. Contact
8. Footer

## Features

- ✅ Fully responsive
- ✅ Matches website's sustainable design
- ✅ Configurable via environment variables
- ✅ Supports iframe and script embeds
- ✅ Shows placeholder when not configured
- ✅ Can be completely disabled

## Styling

The Tarifrechner section:
- Uses white background to match the site
- Has natural green borders (2px solid #E8F5E0)
- Includes proper spacing and padding
- Fully responsive design
- Styled to match the sustainable, nature-connected theme

## Troubleshooting

### Placeholder Showing

If you see a placeholder with "Konfigurieren Sie den Tarifrechner", it means:
- No `TARIFRECHNER_URL` is set (for iframe type)
- No `TARIFRECHNER_SCRIPT` is set (for script type)

**Solution**: Add the appropriate configuration to your `.env` file

### Calculator Not Loading

1. Check that the URL/script is correct
2. Verify the external calculator allows embedding
3. Check browser console for CORS errors
4. Ensure the calculator provider allows iframe/script embedding

### Height Issues

Adjust `TARIFRECHNER_HEIGHT` in `.env` to match your calculator's height requirements.

## Notes

- The section automatically hides if `TARIFRECHNER_ENABLED=False`
- iFrame embeds are generally more reliable than script embeds
- Make sure the external calculator supports your domain for embedding
