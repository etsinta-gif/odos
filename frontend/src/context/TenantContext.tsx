import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { authService, Company } from '../auth/authService';
import { useAuth } from './AuthContext';

type TenantContextType = {
  companies: Company[];
  currentCompany: Company | null;
  setCurrentCompany: (company: Company) => void;
};

const TenantContext = createContext<TenantContextType | undefined>(undefined);

export function TenantProvider({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [currentCompany, setCurrentCompanyState] = useState<Company | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      setCompanies([]);
      setCurrentCompanyState(null);
      return;
    }
    authService.companies().then((rows) => {
      setCompanies(rows);
      if (!rows.length) {
        setCurrentCompanyState(null);
        return;
      }
      const savedId = Number(localStorage.getItem('active_company_id') || 0);
      const selected = rows.find((r) => r.company_id === savedId) || rows[0];
      setCurrentCompanyState(selected);
      localStorage.setItem('active_company_id', String(selected.company_id));
    });
  }, [isAuthenticated]);

  const setCurrentCompany = (company: Company) => {
    setCurrentCompanyState(company);
    localStorage.setItem('active_company_id', String(company.company_id));
  };

  const value = useMemo(
    () => ({ companies, currentCompany, setCurrentCompany }),
    [companies, currentCompany]
  );

  return <TenantContext.Provider value={value}>{children}</TenantContext.Provider>;
}

export function useTenant() {
  const ctx = useContext(TenantContext);
  if (!ctx) {
    throw new Error('useTenant must be used within TenantProvider');
  }
  return ctx;
}
