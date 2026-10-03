create procedure payments_statistics(in date_limit varchar(20))
begin
	(select count(money) as number_paymentys,sum(money) from demo_in_out) as loss_or_not,
    (select sum(money) from demo_in_out where money < 0) as out,
    (select sum(money) from demo_in_out where money >= 0) as in
    from demo_in_out where date like date_limit;
end

create trigger stock_update before update on demo_drugs
for each row
begin:
	if new.package < 0
	then: delete from demo_drugs where product_id=new.product_id;
    end if;
end
update demo_drugs set package=-2 where product_id=1;

create trigger drugs_insert before insert on demo_drugs
for each row
begin:
	if new.package < 0 or new.single_price < 0 or new.single_price < 0 or new.discount > 1 or new.discount < 0
	then: 
	    delete from demo_drugs where product_id=new.product_id;
    end if;
end