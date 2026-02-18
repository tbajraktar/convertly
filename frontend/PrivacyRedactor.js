class PrivacyRedactor {
    constructor() {
        // Regex Patterns
        this.patterns = {
            email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
            creditCard: /\b(?:\d{4}[ -]?){3}\d{4}\b/g,
            phone: /\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\b/g,
            // Simple generic date (YYYY-MM-DD, DD/MM/YYYY, etc.) - compromise handles most relative dates
            date: /\b\d{1,4}[-/]\d{1,2}[-/]\d{2,4}\b/g
        };
    }

    redact(text, intensity = 'medium') {
        let redactedText = text;

        // Level 1: Low (Emails, Credit Cards)
        redactedText = redactedText.replace(this.patterns.email, '████████');
        redactedText = redactedText.replace(this.patterns.creditCard, '████-████-████-████');

        if (intensity === 'low') return redactedText;

        // Level 2: Medium (Phones, Addresses)
        redactedText = redactedText.replace(this.patterns.phone, '███-███-████');

        // Use Compromise for Addresses/Locations (if available)
        if (window.nlp) {
            const doc = window.nlp(redactedText);

            // Redact Places (Cities, Countries, Addresses)
            // We use a custom replacement to preserve length or use a fixed block
            const places = doc.places().out('array');
            places.forEach(place => {
                redactedText = redactedText.replace(new RegExp(`\\b${this.escapeRegExp(place)}\\b`, 'g'), '██████');
            });
        }

        if (intensity === 'medium') return redactedText;

        // Level 3: High (Names, Dates)
        if (window.nlp) {
            const doc = window.nlp(redactedText);

            // Redact People
            const people = doc.people().out('array');
            people.forEach(person => {
                redactedText = redactedText.replace(new RegExp(`\\b${this.escapeRegExp(person)}\\b`, 'g'), '██████');
            });

            // Redact Dates
            const dates = doc.dates().out('array');
            dates.forEach(date => {
                redactedText = redactedText.replace(new RegExp(`\\b${this.escapeRegExp(date)}\\b`, 'g'), '██████');
            });
        }

        // Regex catch-all for numeric dates if NLP missed them
        redactedText = redactedText.replace(this.patterns.date, '██/██/████');

        return redactedText;
    }

    escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
}

// Export global instance
window.PrivacyRedactor = new PrivacyRedactor();
