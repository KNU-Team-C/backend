class Company {
  var id: int;
  var name: string;
  var email: string;
  var address: string;
  var phone_number: string;
  var employees_num: int;
  var logo_url: string;
  var mini_logo_url: string;
  var location: string;
  var description: string;
  var is_blocked: bool;
  var is_verified: bool;
  var date_created: string;

  constructor(
    id: int,
    name: string,
    email: string,
    address: string,
    phone_number: string,
    employees_num: int,
    logo_url: string,
    mini_logo_url: string,
    location: string,
    description: string,
    is_blocked: bool,
    is_verified: bool,
    date_created: string
  ) {
    this.id := id;
    this.name := name;
    this.email := email;
    this.address := address;
    this.phone_number := phone_number;
    this.employees_num := employees_num;
    this.logo_url := logo_url;
    this.mini_logo_url := mini_logo_url;
    this.location := location;
    this.description := description;
    this.is_blocked := is_blocked;
    this.is_verified := is_verified;
    this.date_created := date_created;
  }
  

  
}

class Program {
  var companies: seq<Company>;

  constructor() {
    this.companies := [];
  }

   method isUnique(s: Company) returns (res:bool){
    for i:=0 to |this.companies|
    {
        if this.companies[i].name==s.name 
        {
            return false;
        }
        
    }
    return true;
   }
  
    method LastIndexOf(c: char, s: string)returns(index:int){
        index:=-1;
        for i:=0 to |s|
        {
            if s[i] == c
            {
                index:=i;
            }
        }
        
    }
    method NumberOfChars(c: char, s: string)returns(num:int){
        num:=0;
        for i:=0 to |s|
        {
            if s[i] == c
            {
                num:= num + 1;
            }
        }
        
    }

  method IsValidEmail(email: string) returns (valid: bool)
  
    {
    var atIndex := LastIndexOf('@',email);
    var dotIndex := LastIndexOf('.',email);
    var aNum :=NumberOfChars('@',email);
    valid := atIndex >= 0 && dotIndex > atIndex && dotIndex < |email| - 1 && aNum==1&&|email|>3;
    }
  

  method add_company(   
    name: string,
    email: string,
    address: string,
    phone_number: string,
    employees_num: int,
    logo_url: string,
    mini_logo_url: string,
    location: string,
    description: string
  ) 
    returns (company: Company, unique:bool, created: bool, validEmail:bool)
    modifies this
    requires |this.companies|>=0 && |name|>3 && 16>=|phone_number|>=8
    && forall i::1<i<|phone_number|==> '0'<=phone_number[i]<='9'&&phone_number[0]=='+'
    
    
    ensures (unique && validEmail)== created     
    {
    company := new Company(
      |this.companies|+1,
      name,
      email,
      address,
      phone_number,
      employees_num,
      logo_url,
      mini_logo_url,
      location,
      description,
      false,
      false,
      "date_created"
    );
    validEmail:= IsValidEmail(email);
    unique := this.isUnique(company);
    if( unique && validEmail){
         this.companies := this.companies + [company];
         created:=true;
    }else{
        created:=false;
    }
    
}

  
}