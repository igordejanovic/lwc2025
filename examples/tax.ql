form TaxComputation "Tax computation for 2025" {
    // Basic information
    "Enter your date of birth:"
        birthDate: date

    "Are you filing as a single taxpayer?"
        isSingle: boolean

    if (!isSingle){
        "Are you filing jointly with a spouse?"
            isMarried: boolean
    }

    "Enter your total income:"
        grossIncome: money

    if (!isSingle){
        "Enter your spouse's income (if applicable):"
            spouseIncome: money default 0.00
    }

    // Complex conditional logic
    if (isMarried && !isSingle) {
        "Number of dependents under 18:"
            childDependents: integer range 0..10

        "Number of dependents over 65:"
            elderDependents: integer range 0..5

        "Do you qualify for veteran benefits?"
            isVeteran: boolean

        // Nested conditions
        if (childDependents > 0 || elderDependents > 0) {
            "Childcare expenses:"
                childcareExpenses: money

            "Elder care expenses:"
                elderCareExpenses: money

            // Complex calculated field with multiple dependencies
            "Deduction allowance:"
                dependentsAllowance = (childDependents * 2000) +
                                     (elderDependents * 1500) +
                                     (childcareExpenses * 0.3) +
                                     (elderCareExpenses * 0.25)
        }
    }

    // Another branch with complex conditions
    if ((isSingle && grossIncome > 50000) ||
        (isMarried && (grossIncome + spouseIncome) > 100000)) {

        "Enter capital gains amount:"
            capitalGains: money

        "Enter retirement contributions:"
            retirementContributions: money

        // Multi-step calculation
        "Adjusted taxable income:"
            adjustedIncome = grossIncome + spouseIncome - retirementContributions

        "Capital gains tax liability:"
            capitalGainsTax = if capitalGains > 50000 then capitalGains * 0.20
                             else if capitalGains > 20000 then capitalGains * 0.15
                             else capitalGains * 0.10
    }

    // Final calculation that depends on previous fields
    "Estimated tax liability:"
        estimatedTax = if isMarried && dependentsAllowance > 1000
                       then (adjustedIncome - dependentsAllowance) * 0.25 + capitalGainsTax
                      else if isSingle
                       then adjustedIncome * 0.30 + capitalGainsTax
                      else grossIncome * 0.20 + capitalGainsTax

    "If you have additional data write here:"
        additionalInfo: string
}
